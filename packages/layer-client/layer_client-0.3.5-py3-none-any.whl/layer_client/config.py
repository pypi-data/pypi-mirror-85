from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DataCatalogConfig:
    host: str
    port: int
    s3_bucket_name: str

    @property
    def is_enabled(self) -> bool:
        return bool(self.host)

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"


@dataclass(frozen=True)
class ModelCatalogConfig:
    host: str
    port: int

    @property
    def is_enabled(self) -> bool:
        return bool(self.host)

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"


@dataclass(frozen=True)
class LayerClientConfig:
    organization_id: UUID
    user_id: UUID
    client_id: UUID
    data_catalog: DataCatalogConfig
    model_catalog: ModelCatalogConfig
