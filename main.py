from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from checkers.checkers import Checkers
from checkers.tui.ConnectionManager import ConnectionManager

app = FastAPI(title="Checkers Engine")
manager = ConnectionManager()
game = Checkers()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/game", response_model=None)
def get_game() -> Checkers:
    return game


# Visit http://localhost:8000/ws and send a test message.
# Open it again in another tab and then close the tab.
@app.get("/ws")
async def ws():
    from checkers.tui.websocket_html import html
    return HTMLResponse(html)


@app.websocket("/communicate/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"Received:{data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
