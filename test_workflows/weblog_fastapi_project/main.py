import logging
from typing import Optional

import plotly.graph_objects as go
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

class WeblogTrace(BaseModel):
    task_id: int
    status: str
    hash: str
    name: str
    exit: Optional[int] # POSIX process exit status
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
            return int(self.name[self.name.find("(")+1:self.name.rfind(")")])
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
    metadata: Optional[WeblogMetadata] # only apperas in completed message

    
process_messages: list[WeblogStructure] = []
overall_messages: list[WeblogStructure] = []



@app.get("/")
async def root():
    return {"messages": process_messages}

@app.post("/weblog")
def post_weblog_nextflow(data: WeblogStructure):
    if not "process" in data.event:
        overall_messages.append(data)
    else:
        process_messages.append(data)
    
@app.get("/progress", response_class=HTMLResponse)    
def create_progress_picture():
    print(len(process_messages))
    print([x.trace.name for x in process_messages])
    print([x.trace.nth_process for x in process_messages])
    print([x.utcTime for x in process_messages])
    
    fig = go.Figure(data = [go.Scatter(
        y=[x.trace.name for x in process_messages],
        x=[x.utcTime for x in process_messages],
        text=[[x.trace.nth_process, x.event] for x in process_messages],
        textposition="top center", 
        mode="markers")])
    
    return fig.to_html()

@app.get("/process")
def filter_messages_per_process(hash: Optional[str] = None):
    if not hash:
        return {x.trace.hash : [y for y in process_messages if x.trace.hash == y.trace.hash] 
                for x in process_messages if x.event == "process_started" 
                }
 
@app.get("/none_process_messages")
def filter_none_process_messages(filter = None):
    if not filter:
        return overall_messages   
