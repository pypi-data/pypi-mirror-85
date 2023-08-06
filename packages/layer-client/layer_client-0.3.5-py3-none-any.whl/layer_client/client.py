import json
import time
from contextlib import ExitStack, contextmanager
from logging import Logger
from typing import Any, Iterator, Optional, Union

import grpc
from pandas import DataFrame as PDataFrame
from pyspark.sql import DataFrame as SDataFrame, SparkSession

from .api.entity.dataset_build_pb2 import DatasetBuild
from .api.ids_pb2 import AppId, UserId
from .api.service.datacatalog.data_catalog_api_pb2 import (
    CompleteBuildRequest,
    GetLatestBuildRequest,
    InitiateBuildRequest,
)
from .api.service.datacatalog.data_catalog_api_pb2_grpc import DataCatalogAPIStub
from .api.service.modelcatalog.model_catalog_api_pb2_grpc import ModelCatalogAPIStub
from .api.value.storage_location_pb2 import StorageLocation
from .config import LayerClientConfig
from .exceptions import LayerClientException
from .mlmodels.service import MLModelService, ModelDefinition


_MAX_FAILURE_INFO_LENGTH = 200


class DataCatalogClient:
    _service: DataCatalogAPIStub

    def __init__(
        self, config: LayerClientConfig, logger: Logger, session: SparkSession
    ):
        self._user_id = config.user_id
        self._client_id = config.client_id
        self._config = config.data_catalog
        self._session = session
        self._logger = logger

    @contextmanager
    def init(self) -> Iterator["DataCatalogClient"]:
        with grpc.insecure_channel(self._config.address) as channel:
            self._service = DataCatalogAPIStub(channel)  # type: ignore
            yield self

    def load(self, name: str, version: Optional[str] = None) -> SDataFrame:
        self._logger.debug(
            "Loading data object with name %r and version %r", name, version
        )
        resp = self._service.GetLatestBuild(
            GetLatestBuildRequest(
                app_id=AppId(value=str(self._client_id)),
                dataset_name=name,
                dataset_version=version,
            )
        )
        return self._session.read.parquet(resp.build.location.uri)

    def save(
        self,
        name: str,
        obj: Union[PDataFrame, SDataFrame],
        version: Optional[str] = None,
    ) -> DatasetBuild:  # type: ignore
        self._logger.debug(
            "Saving data object with name %r and version %r", name, version
        )
        df: SDataFrame
        if isinstance(obj, PDataFrame):
            df = self._session.createDataFrame(obj)
        else:
            df = obj

        schema = json.dumps(df.schema.jsonValue())
        init_resp = self._service.InitiateBuild(
            InitiateBuildRequest(
                app_id=AppId(value=str(self._client_id)),
                dataset_name=name,
                dataset_version=version or "",
                build_description="",
                format="parquet",
                user=UserId(value=str(self._user_id)),
                schema=schema,
                current_timestamp=int(time.time()),
            )
        )

        uri = f"s3a://{self._config.s3_bucket_name}/{init_resp.suggested_path}"
        exception: Optional[Exception] = None
        try:
            df.write.mode("overwrite").parquet(uri)
        except Exception as exc:
            exception = exc
            comp_req = CompleteBuildRequest(
                id=init_resp.id,
                current_timestamp=int(time.time()),
                status=DatasetBuild.BuildStatus.BUILD_STATUS_FAILED,  # type: ignore
                failure=CompleteBuildRequest.BuildFailed(  # type: ignore
                    info=str(exc)[:_MAX_FAILURE_INFO_LENGTH]
                ),
            )
        else:
            comp_req = CompleteBuildRequest(
                id=init_resp.id,
                current_timestamp=int(time.time()),
                status=DatasetBuild.BuildStatus.BUILD_STATUS_COMPLETED,  # type: ignore
                success=CompleteBuildRequest.BuildSuccess(  # type: ignore
                    location=StorageLocation(uri=uri)
                ),
            )

        comp_resp = self._service.CompleteBuild(comp_req)

        if exception:
            raise exception

        return comp_resp.build


class ModelCatalogClient:
    _service: ModelCatalogAPIStub

    def __init__(
        self,
        config: LayerClientConfig,
        ml_model_service: MLModelService,
        logger: Logger,
    ):
        self._client_id = config.client_id
        self._config = config.model_catalog
        self._org_id = config.organization_id
        self._logger = logger
        self._ml_model_service = ml_model_service

    @contextmanager
    def init(self) -> Iterator["ModelCatalogClient"]:
        with grpc.insecure_channel(self._config.address) as channel:
            self._service = ModelCatalogAPIStub(channel)  # type: ignore
            yield self

    def load(
        self, name: str, version: Optional[int] = None, build: Optional[int] = None
    ) -> Any:
        """
        Loads a model from the model catalog

        :param name: the name of the model
        :param version: the version of the model
        :param build: the build number of the model
        :return: a model definition
        """
        self._logger.debug(f"Loading model object with name {name}")
        model_definition = ModelDefinition(self._org_id, model_name=name)
        return self._ml_model_service.retrieve(
            model_definition, version=version, build=build
        )

    def save(
        self,
        name: str,
        obj: Any,
        owner: str,
        version: Optional[int] = None,
        model_input: Any = None,
        model_output: Any = None,
    ) -> Any:
        organization_id = self._org_id
        mlflow_model_name = self._ml_model_service.get_next_model_version(
            str(organization_id), name, version
        )
        self._logger.debug(f"Storing given model {obj} with name {mlflow_model_name}")
        flavor = self._ml_model_service.get_model_flavor(obj)
        if not flavor:
            raise LayerClientException("Model flavor not found")
        model_definition = ModelDefinition(
            organization_id=organization_id,
            model_name=name,
            mlflow_model_name=mlflow_model_name,
        )
        self._ml_model_service.store(
            model_definition,
            obj,
            model_input,
            model_output,
            flavor,
            owner,
            str(self._client_id),
        )
        return obj

    def log_parameter(self, key: str, value: str) -> None:
        """
        Logs given parameter to the model storage service

        :param key: name of the parameter
        :param value: value of the parameter
        """
        self._ml_model_service.log_parameter(str(self._client_id), key, value)

    def log_metric(self, key: str, value: float) -> None:
        """
        Logs given metric to the model storage service

        :param key: name of the metric
        :param value: value of the metric
        """
        self._ml_model_service.log_metric(str(self._client_id), key, value)


class LayerClient:
    def __init__(
        self, config: LayerClientConfig, logger: Logger, session: SparkSession
    ):
        self._config = config
        self._data_catalog = DataCatalogClient(config, logger, session)
        ml_model_service = MLModelService(logger)
        self._model_catalog = ModelCatalogClient(config, ml_model_service, logger)

    @contextmanager
    def init(self) -> Iterator["LayerClient"]:
        with ExitStack() as exit_stack:
            if self._config.data_catalog.is_enabled:
                exit_stack.enter_context(self._data_catalog.init())
            if self._config.model_catalog.is_enabled:
                exit_stack.enter_context(self._model_catalog.init())
            yield self

    @property
    def data_catalog(self) -> DataCatalogClient:
        return self._data_catalog

    @property
    def model_catalog(self) -> ModelCatalogClient:
        return self._model_catalog
