from contextlib import contextmanager
from typing import Iterator

from .service import MLModelService


@contextmanager
def ml_model_run(notebook_id: str, service: MLModelService) -> Iterator[None]:
    if not service.active_runs:
        service.start_run(notebook_id=notebook_id)
    yield
