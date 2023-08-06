import ast
import importlib
from logging import Logger
from typing import Any, Dict, Optional

import mlflow
from mlflow.entities import Experiment, Run
from mlflow.entities.model_registry import ModelVersion
from mlflow.exceptions import RestException
from mlflow.models.signature import infer_signature
from mlflow.tracking import MlflowClient
from mlflow.tracking.fluent import ActiveRun
from mlflow.utils.mlflow_tags import MLFLOW_SOURCE_TYPE

from layer_client.exceptions import LayerClientException
from layer_client.mlmodels import ModelObject, flavors

from .flavors import ModelFlavor
from .flavors.flavor import ModelDefinition


class MLModelService:
    """
    Handles ML model lifecycle within the application. Users of this service can
    store/load/delete ML models.
    """

    def __init__(self, logger: Logger):
        self.logger = logger
        self.client = MlflowClient()
        self.active_runs: Dict[str, Run] = {}

    def start_run(self, notebook_id: str) -> None:
        """
        Starts an MLFlow run for specified notebook

        Args:
            notebook_id: notebook id to be associated with the run
        """
        experiment = self.__get_or_create_experiment(notebook_id)
        active_run: Run = self.__create_run(experiment_id=experiment.experiment_id)
        self.active_runs[notebook_id] = active_run

    def end_run(self, notebook_id: str) -> None:
        """
        Marks the active MLFlow run as finished for specified notebook

        Args:
            notebook_id: notebook id which corresponding run would be marked as finished
        """
        active_run = self.active_runs[notebook_id]
        run_id = active_run.info.run_id
        self.client.set_terminated(run_id=run_id)
        del self.active_runs[notebook_id]

    def log_parameter(self, notebook_id: str, key: str, value: str) -> None:
        active_run = self.active_runs[notebook_id]
        self.client.log_param(active_run.info.run_id, key, value)

    def log_metric(self, notebook_id: str, key: str, value: float) -> None:
        active_run = self.active_runs[notebook_id]
        self.client.log_metric(active_run.info.run_id, key, value)

    def get_next_model_version(
        self, organization_id: str, name: str, version: Optional[int] = None
    ) -> str:
        """
        Get updated model name by adding the model version information

        Args:
            organization_id: Organization id
            name: Model name assigned by the end-user
            version: Version value of corresponding model
        Returns:
            Model name with version
        """
        name_with_organization = organization_id + "_" + name
        if version is None:
            models = self.client.search_registered_models(
                filter_string=f"name LIKE '{name_with_organization}%'",
                order_by=["name DESC"],
                max_results=1,
            )
            model = models[0] if models else None
            return (
                model.latest_versions[0].name
                if model is not None
                else name_with_organization + "_version1"
            )
        else:
            return name_with_organization + "_version" + str(version)

    # pytype: disable=annotation-type-mismatch # https://github.com/google/pytype/issues/640
    def store(
        self,
        model_definition: ModelDefinition,
        model_object: ModelObject,
        model_input: Any,
        model_output: Any,
        flavor: ModelFlavor,
        owner: str,
        notebook_id: str,
    ) -> None:  # pytype: enable=annotation-type-mismatch
        """
        Stores given model object along with its definition to the backing storage.
        The metadata written to db and used later on whilst loading the ML model.

        Args:
            model_definition: Model metadata object which describes the model instance
            model_object: Model object to be stored
            model_input: Model input (training) data
            model_output: Model output (prediction) data
            flavor: Corresponding flavor information of the model object
            owner: the owner of the model. Currently considered to be the user who first saved it.
            notebook_id: ID of the notebook which model originated from
        Returns:
            bool operation status indicator
        """
        if notebook_id not in self.active_runs:
            self.start_run(notebook_id)
        active_run = self.active_runs[notebook_id]
        mlflow.tracking.fluent._active_run_stack.append(  # pylint: disable=protected-access
            ActiveRun(active_run)
        )
        path = model_definition.model_organization_id
        self.logger.debug(
            f"Saving user model {model_definition.mlflow_model_name}({model_object}) on path {path}"
        )
        if model_output is not None and model_input is None:
            raise LayerClientException(
                "Model input not found! Model output can be assigned only if model input is assigned"
            )
        signature = (
            infer_signature(model_input, model_output).to_dict()
            if model_input is not None
            else None
        )
        active_run_id = active_run.info.run_id
        is_model_structure_compatible = self.__is_compatible(
            model_definition.mlflow_model_name, signature, active_run_id
        )
        self.end_run(notebook_id)
        self.start_run(notebook_id)
        if is_model_structure_compatible:
            try:
                tags = {
                    "name": model_definition.model_name,
                    "owner": owner,
                    "review_status": "REVIEW_STATUS_PENDING",
                    "parent_app": notebook_id,
                    "organization_id": model_definition.model_organization_id,
                    "module_name": flavor.metadata.module_name,
                    "class_name": flavor.metadata.class_name,
                    "signature": signature,
                }
                flavor.save(
                    model_definition,
                    model_object,
                    active_run_id,
                    tags=tags,
                )
                self.logger.debug(f"Writing model {model_definition} metadata")
            except Exception as ex:
                raise LayerClientException(f"Error while storing model, {ex}")
            else:
                self.logger.debug(
                    f"User model {model_definition.mlflow_model_name} saved successfully on path {path}"
                )
        else:
            raise LayerClientException(
                "Model signature, metrics or parameters are incompatible"
            )

    def retrieve(
        self,
        model_definition: ModelDefinition,
        version: Optional[int] = None,
        build: Optional[int] = None,
    ) -> ModelObject:
        """
        Retrieves the given model definition from the storage and returns the actual
        model object

        Args:
            model_definition: Model metadata object which describes the model instance
            version: model version to load
            build: model version's build to load
        Returns:
            Loaded model object

        """
        self.logger.debug(
            f"User requested to load model {model_definition.model_name} "
            f"with version {version} "
            f"with build {build}"
        )
        path = model_definition.model_organization_id
        model_version = self.search_model(
            model_definition.model_organization_id,
            model_definition.model_name,
            version=version,
            build=build,
        )
        if model_version is None:
            raise LayerClientException(
                f"Model named {model_definition.model_name} not found"
            )
        self.logger.debug(
            f"Loading model {model_definition.model_name} from path {path}"
        )
        module = importlib.import_module(model_version.tags["module_name"])
        model_flavor_class = getattr(module, model_version.tags["class_name"])
        return model_flavor_class().load(
            model_name=model_version.name, version=model_version.version
        )

    def delete(self, model_definition: ModelDefinition) -> None:
        """
        Deletes the model along with its metadata from the storage

        Args:
            model_definition: Model metadata object which describes the model instance
        """
        self.logger.debug(
            f"User requested to delete model {model_definition.model_name}"
        )
        self.client.delete_registered_model(name=model_definition.model_name)
        self.logger.debug(f"Deleted model {model_definition.model_name}")

    def search_model(
        self,
        organization_id: str,
        name: str,
        version: Optional[int] = None,
        build: Optional[int] = None,
    ) -> Optional[ModelVersion]:
        """
        Search models in the model registry by converting the user assigned model name into
        model name with version format

        Args:
            organization_id: Organization id
            name: User assigned model name
            version: Version of the corresponding model
            build: Build number of the corresponding model
        Returns:
            ModelVersion object of the searched model
        """
        if version is not None and build is not None:
            model_name = organization_id + "_" + name + "_version" + str(version)
            models = self.client.search_model_versions(
                filter_string=f"name = '{model_name}'"
            )
            build_exists = models and models[-1].version >= str(build)
            return models[build - 1] if build_exists else None

        elif version is not None and build is None:
            model_name = organization_id + "_" + name + "_version" + str(version)
            models = self.client.search_registered_models(
                filter_string=f"name = '{model_name}'", max_results=1
            )
            return models[0].latest_versions[0] if models else None

        else:
            models = self.client.search_registered_models(
                filter_string=f"name LIKE '{organization_id + '_' + name}_version%'",
                order_by=["name DESC"],
                max_results=1,
            )
            return models[0].latest_versions[0] if models else None

    @staticmethod
    def get_model_flavor(model_object: ModelObject) -> Optional[ModelFlavor]:
        """
        Checks if given model objects has a known model flavor and returns
        the flavor if there is a match.

        Args:
            model_object: User supplied model object

        Returns:
            The corresponding model flavor if there is match

        Raises:
            LayerException if user provided object does not have a known flavor.

        """
        flavor = MLModelService.__check_and_get_flavor(model_object)
        if flavor is None:
            raise LayerClientException(f"Unexpected model type {type(model_object)}")
        return flavor

    @staticmethod
    def check_object_has_known_flavor(model_object: ModelObject) -> bool:
        """
        Checks whether given model has a known flavor which we can work with

        Args:
            model_object: A machine learning model which could be originated
            from any framework

        Returns:
            bool result
        """
        flavor = MLModelService.__check_and_get_flavor(model_object)
        return flavor is not None

    @staticmethod
    def __check_and_get_flavor(model_object: ModelObject) -> Optional[ModelFlavor]:
        for model_flavor in flavors.MODEL_FLAVORS:
            if model_flavor.can_interpret_object(model_object):
                return model_flavor
        return None

    def __get_or_create_experiment(self, experiment_name: str) -> Experiment:
        should_create = False
        experiment = None
        try:
            experiment = self.client.get_experiment_by_name(experiment_name)
            if experiment is None:
                should_create = True
        except RestException:
            should_create = True
        if should_create:
            experiment_id = self.client.create_experiment(experiment_name)
            experiment = self.client.get_experiment(experiment_id)
        return experiment

    def __create_run(self, experiment_id: str) -> Run:
        tags = {
            MLFLOW_SOURCE_TYPE: "NOTEBOOK",
        }
        run = self.client.create_run(experiment_id=experiment_id, tags=tags)
        return run

    def __is_compatible(
        self, model_name: str, signature: Dict[str, str], active_run_id: str
    ) -> bool:
        model_name_components = self.__split_extended_model_name(model_name)
        latest_model = self.search_model(
            model_name_components["organization_id"],
            model_name_components["model_name"],
            int(model_name_components["version"]),
        )
        if latest_model is None:
            return True
        else:
            latest_model_signature = latest_model.tags["signature"]
            latest_model_metrics = self.__get_model_metrics(latest_model.run_id)
            latest_model_parameters = self.__get_model_parameters(latest_model.run_id)
            is_compatible = self.__compare_model_structure(
                active_run_id,
                signature,
                latest_model_signature,
                latest_model_metrics,
                latest_model_parameters,
            )
            return is_compatible

    def __compare_model_structure(
        self,
        active_run_id: str,
        signature: Dict[str, str],
        latest_model_signature: str,
        latest_model_metrics: Dict[str, str],
        latest_model_parameters: Dict[str, str],
    ) -> bool:
        metrics = self.__get_model_metrics(active_run_id)
        parameters = self.__get_model_parameters(active_run_id)
        is_metric_compatible = set(metrics.keys()) == set(latest_model_metrics.keys())
        is_parameter_compatible = set(parameters.keys()) == set(
            latest_model_parameters.keys()
        )
        is_signature_compatible = signature == ast.literal_eval(latest_model_signature)

        return (
            is_signature_compatible and is_metric_compatible and is_parameter_compatible
        )

    def __split_extended_model_name(self, extended_model_name: str) -> Dict[str, str]:
        version = extended_model_name.split("_version")[1]
        organization_id = extended_model_name.split("_")[0]
        model_name = extended_model_name.replace(organization_id + "_", "").replace(
            "_version" + version, ""
        )

        return {
            "organization_id": organization_id,
            "model_name": model_name,
            "version": version,
        }

    def __get_model_metrics(self, run_id: str) -> Dict[str, str]:
        return self.client.get_run(run_id).data.metrics

    def __get_model_parameters(self, run_id: str) -> Dict[str, Any]:
        return self.client.get_run(run_id).data.params
