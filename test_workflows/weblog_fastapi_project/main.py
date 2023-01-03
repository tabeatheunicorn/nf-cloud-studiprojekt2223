import asyncio
import logging
from typing import Optional

import plotly.graph_objects as go
from connection_manager import ConnectionManager
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from html_string import html
from pydantic import BaseModel
from weblog.weblog_datastructures import WeblogListStructure, WeblogStructure

app = FastAPI()

manager = ConnectionManager()

process_messages: WeblogListStructure = []
overall_messages: WeblogListStructure = []

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )

@app.get("/")
async def root():
    return {"messages": process_messages}


@app.post("/weblog")
async def post_weblog_nextflow(data: WeblogStructure):
    if not "process" in data.event:
        overall_messages.append(data)
    else:
        process_messages.append(data)
    await manager.broadcast(data.json())
    print("Broadcast done")


@app.get("/progress", response_class=HTMLResponse)
def create_progress_picture():
    print(len(process_messages))
    print([x.trace.name for x in process_messages])
    print([x.trace.nth_process for x in process_messages])
    print([x.utcTime for x in process_messages])

    fig = go.Figure(
        data=[
            go.Scatter(
                y=[x.trace.name for x in process_messages],
                x=[x.utcTime for x in process_messages],
                text=[[x.trace.nth_process, x.event] for x in process_messages],
                textposition="top center",
                mode="markers",
            )
        ]
    )

    return fig.to_html()


@app.get("/process")
def filter_messages_per_process(hash: Optional[str] = None):
    if not hash:
        return {
            x.trace.hash: [y for y in process_messages if x.trace.hash == y.trace.hash]
            for x in process_messages
            if x.event == "process_started"
        }


@app.get("/wspage")
async def get_websocket_testpage():
    return HTMLResponse(html)


async def keep_alive(websocket: WebSocket, interval: float):
    while True:
        await websocket.keep_alive(interval=interval)
        await asyncio.sleep(interval)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        for message in process_messages:
            await manager.send_personal_message(message=message.json(), websocket=websocket)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
