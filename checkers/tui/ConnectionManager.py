from fastapi import WebSocket
from fastapi.templating import Jinja2Templates
import jinja2

class ConnectionManager:
    def __init__(self, templates: Jinja2Templates):
        self.active_connections: list[WebSocket] = []
        self.templates: Jinja2Templates = templates
        self.messages: list[str] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        self.messages.append(message)

        response_template: jinja2.Template = self.templates.get_template(name="websocket_response.html")
        response = response_template.render(messages = self.messages)
        for connection in self.active_connections:
            await connection.send_text(response)
