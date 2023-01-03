from typing import Optional

from pydantic import BaseModel


class WeblogTrace(BaseModel):
    task_id: int
    status: str
    hash: str
    name: str
    exit: Optional[int]  # POSIX process exit status
    submit: Optional[int]
    start: Optional[int]
    complete: Optional[int]
    process: Optional[str]
    duration: Optional[float]
    tag: Optional[str]
    attempt: Optional[int]
    native_id: Optional[int]

    @property
    def nth_process(self) -> int:
        if "(" in self.name:
            return int(self.name[self.name.find("(") + 1 : self.name.rfind(")")])
        else:
            return 0


class WeblogMetadata(BaseModel):
    parameters: dict
    workflow: dict


class WeblogStructure(BaseModel):
    runName: str
    runId: str
    event: str
    utcTime: str
    trace: Optional[WeblogTrace]
    metadata: Optional[WeblogMetadata]  # only apperas in completed message
