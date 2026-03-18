from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .engine import Checkers, main_loop
from .ConnectionManager import ConnectionManager


app = FastAPI(title="Checkers Engine")
templates = Jinja2Templates(directory="templates")


manager = ConnectionManager(templates)
game = Checkers()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/playertwo", response_class=HTMLResponse)
async def playertwo(request: Request):
    return templates.TemplateResponse(request=request, name="playertwo.html", context={})


@app.get("/game", response_model=None)
def get_game() -> Checkers:
    return game


@app.websocket("/communicate/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    # TODO: Startup 'watcher' async func that will poll and enforce timers/turn time limits
    # by reading from the shared game object

    try:
        await main_loop(game, manager, websocket, client_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
    except Exception as err:
        print(f"Unexpected Server Error, err={err}")
        await manager.broadcast(f"Unexepected Server Error")
