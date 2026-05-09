
from typing import Protocol, runtime_checkable, Any

@runtime_checkable
class DataSink(Protocol):
    def write(self, data: dict) -> None:
        ...

@runtime_checkable
class PipelineService(Protocol):
    def execute(self, raw_data: Any) -> None:
        ...
