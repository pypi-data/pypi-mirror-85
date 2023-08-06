import re
import unicodedata
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, NamedTuple, Optional
from uuid import UUID, uuid4

import keras  # type: ignore
import lightgbm  # type: ignore
import tensorflow  # type: ignore
import torch
import xgboost  # type: ignore
from mlflow.exceptions import MlflowException
from mlflow.models import Model as MLFlowModel
from mlflow.protos.databricks_pb2 import RESOURCE_ALREADY_EXISTS, ErrorCode
from mlflow.store.artifact.runs_artifact_repo import RunsArtifactRepository
from mlflow.tracking import MlflowClient
from mlflow.tracking.fluent import log_artifacts
from mlflow.utils.file_utils import TempDir
from pyspark.ml.util import MLWritable
from sklearn.base import BaseEstimator  # type: ignore

from layer_client.mlmodels import ModelObject


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.

    Taken unchanged from django/utils/text.py
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)


class ModelDefinition:
    """Holds information regarding an ML model.

    This class holds structural information about an ML Model and is able to construct a path where you
    can find the model in the storage.
    """

    def __init__(
        self,
        organization_id: UUID,
        model_name: str,
        mlflow_model_name: Optional[str] = None,
    ):
        self.__model_organization_id = str(organization_id)
        self.__model_name = slugify(model_name).replace("-", "")
        self.__mlflow_model_name = mlflow_model_name

    @property
    def model_organization_id(self) -> str:
        """Returns the model organization id

        This id uniquely identifies the ML Model in the storage engine and can be used for a look-up

        Returns:
            A string path
        """
        return self.__model_organization_id

    @property
    def model_name(self) -> str:
        """Returns the model name

        Returns:
            A string name
        """
        return self.__model_name

    @property
    def mlflow_model_name(self) -> str:
        """Returns the mlflow model name

        Returns:
            A string mlflow model name
        """
        return self.__mlflow_model_name

    def __repr__(self) -> str:
        return (
            f"ModelDefinition{{"
            f"model_organization_id: {self.model_organization_id}, "
            f"mlflow_model_name: {self.mlflow_model_name}, "
            f"model_name:{self.model_name}"
            f"}}"
        )


class ModelFlavorMetaData(NamedTuple):
    """NamedTuple containing flavor module and class names"""

    module_name: str
    class_name: str


class ModelFlavor(metaclass=ABCMeta):
    """Represents a machine learning model flavor for a specific framework.

    Implementations provide methods for checking for membership, saving and loading
    of machine learning models within their flavor.
    """

    @abstractmethod
    def model_class(self) -> type:
        """Defines the class that this Model Flavor uses to check for compatibility.

        Returns:
            type: A class reference of the model type to check for.
        """

    @abstractmethod
    def log_model_impl(self) -> Any:
        """Defines the method that this Model Flavor uses to log(/store) a model.

        Returns:
             A method reference of the model log implementation.
        """

    @abstractmethod
    def load_model_impl(self) -> Any:
        """Defines the method that this Model Flavor uses to load a model.

        Returns:
             A method reference of the model loader implementation.
        """

    def can_interpret_object(self, model_object: ModelObject) -> bool:
        """Checks whether supplied model object has flavor of this class.

        Args:
            model_object: A machine learning model which could be originated from any framework.

        Returns:
            bool: true if this ModelFlavor can interprete the given model instance.
        """
        return isinstance(model_object, self.model_class())

    def save(
        self,
        model_definition: ModelDefinition,
        model_object: ModelObject,
        run_id: str,
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        """Stores the given machine learning model definition to the backing store.

        Args:
            model_definition: Model metadata object which describes the model instance
            model_object: A machine learning model which could be originated from any framework
            run_id: MLFlow Run ID to be used to associate the model with the run
            tags: tags to add to the ml model
        """
        artifact_path = f"{model_definition.mlflow_model_name}-{uuid4()}"
        model_impl = self.log_model_impl()

        with TempDir() as tmp:
            local_path = tmp.path("model")
            mlflow_model = MLFlowModel()
            mlflow_model.run_id = run_id
            mlflow_model.artifact_path = artifact_path
            model_impl(model_object, path=local_path, mlflow_model=mlflow_model)
            log_artifacts(local_path, artifact_path)
            #  We are accessing internal method since we need to record model to a
            #  specific run_id which is managed by us.
            MlflowClient()._record_logged_model(  # pylint: disable=protected-access
                run_id, mlflow_model
            )
            model_name = model_definition.mlflow_model_name
            if model_name is not None:
                self.register_model(artifact_path, model_name, run_id, tags)

    def register_model(
        self,
        artifact_path: str,
        model_name: str,
        run_id: str,
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        client = MlflowClient()
        try:
            client.create_registered_model(model_name, tags=tags)
        except MlflowException as e:
            if e.error_code != ErrorCode.Name(RESOURCE_ALREADY_EXISTS):
                raise e
        model_uri = "runs:/%s/%s" % (run_id, artifact_path)
        source = RunsArtifactRepository.get_underlying_uri(model_uri)
        (run_id, _) = RunsArtifactRepository.parse_runs_uri(model_uri)
        client.create_model_version(model_name, source, run_id, tags=tags)

    def load(self, model_name: str, version: Optional[str] = None) -> ModelObject:
        """Loads the given machine learning model definition from the backing store and returns an instance of it

        Args:
            model_name: Model name of the model instance
            version: Model version of the model instance

        Returns:
            A machine learning model object
        """
        model_impl = self.load_model_impl()
        return model_impl(f"models:/{model_name}/{version}")

    @property
    def metadata(self) -> ModelFlavorMetaData:
        """Returns metadata which contains flavor module and classname to be used when loading an instance of a flavor

        Returns:
            ModelFlavorMetaData: a metadata dict
        """
        return ModelFlavorMetaData(
            module_name=self.__module__, class_name=self.__class__.__qualname__
        )


class SparkMLModelFlavor(ModelFlavor):
    """Spark ML Model flavor implementation which handles persistence of ML models in `pyspark.ml` package."""

    def model_class(self) -> type:
        return MLWritable

    def log_model_impl(self) -> Any:
        import mlflow.spark

        return mlflow.spark.save_model

    def load_model_impl(self) -> Any:
        import mlflow.spark

        return mlflow.spark.load_model


class ScikitLearnModelFlavor(ModelFlavor):
    """An ML Model flavor implementation which handles persistence of Scikit Learn Models."""

    def model_class(self) -> type:
        return BaseEstimator

    def log_model_impl(self) -> Any:
        import mlflow.sklearn

        return mlflow.sklearn.save_model

    def load_model_impl(self) -> Any:
        import mlflow.sklearn

        return mlflow.sklearn.load_model


class PyTorchModelFlavor(ModelFlavor):
    """An ML Model flavor implementation which handles persistence of PyTorch Models."""

    def model_class(self) -> type:
        return torch.nn.Module

    def log_model_impl(self) -> Any:
        import mlflow.pytorch

        return mlflow.pytorch.save_model

    def load_model_impl(self) -> Any:
        import mlflow.pytorch

        return mlflow.pytorch.load_model


class XGBoostModelFlavor(ModelFlavor):
    """An ML Model flavor implementation which handles persistence of XGBoost Models.

    Uses XGBoost model (an instance of xgboost.Booster).

    """

    def model_class(self) -> type:
        return xgboost.Booster

    def log_model_impl(self) -> Any:
        import mlflow.xgboost

        return mlflow.xgboost.save_model

    def load_model_impl(self) -> Any:
        import mlflow.xgboost

        return mlflow.xgboost.load_model


class LightGBMModelFlavor(ModelFlavor):
    """An ML Model flavor implementation which handles persistence of LightGBM Models.
    Uses LightGBM model (an instance of lightgbm.Booster).

    """

    def model_class(self) -> type:
        return lightgbm.Booster

    def log_model_impl(self) -> Any:
        import mlflow.lightgbm

        return mlflow.lightgbm.save_model

    def load_model_impl(self) -> Any:
        import mlflow.lightgbm

        return mlflow.lightgbm.load_model


class TensorFlowModelFlavor(ModelFlavor):
    """An ML Model flavor implementation which handles persistence of TensorFlow Models."""

    def save(
        self,
        model_definition: ModelDefinition,
        model_object: ModelObject,
        run_id: str,
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        """See ModelFlavor.save()'s documentation.

        Due to peculiar arguments required for mlflow.tensorflow.save_model, we need to duplicate a lot of code here.

        TODO: Refactor this
        """
        artifact_path = f"{model_definition.mlflow_model_name}-{uuid4()}"
        model_impl = self.log_model_impl()

        with TempDir() as tmp:
            local_path = tmp.path("model")
            mlflow_model = MLFlowModel()
            mlflow_model.run_id = run_id
            mlflow_model.artifact_path = artifact_path
            tmp_save_path = tmp.path(
                model_definition.model_organization_id, model_definition.model_name
            )
            tensorflow.saved_model.save(model_object, tmp_save_path)
            model_impl(
                tf_saved_model_dir=tmp_save_path,
                tf_meta_graph_tags=None,
                tf_signature_def_key="serving_default",
                path=local_path,
            )
            log_artifacts(local_path, artifact_path)
            #  We are accessing internal method since we need to record model to a
            #  specific run_id which is managed by us.
            MlflowClient()._record_logged_model(  # pylint: disable=protected-access
                run_id, mlflow_model
            )
            model_name = model_definition.mlflow_model_name
            if model_name is not None:
                self.register_model(artifact_path, model_name, run_id, tags)

    def model_class(self) -> type:
        return tensorflow.Module

    def log_model_impl(self) -> Any:
        import mlflow.tensorflow

        return mlflow.tensorflow.save_model

    def load_model_impl(self) -> Any:
        import mlflow.tensorflow

        return mlflow.tensorflow.load_model


class KerasModelFlavor(ModelFlavor):
    """An ML Model flavor implementation which handles persistence of Keras Models."""

    def model_class(self) -> type:
        return keras.models.Sequential

    def log_model_impl(self) -> Any:
        import mlflow.keras

        return mlflow.keras.save_model

    def load_model_impl(self) -> Any:
        import mlflow.keras

        return mlflow.keras.load_model
