from typing import Annotated

import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi import Depends, WebSocketException, status


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = FastAPI()


def get_html(user_id: int) -> str:
    html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/%d-%d`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
""" % (user_id, (user_id + 1) % 2)
    return html


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, client_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, websocket: WebSocket):
        for key in list(self.active_connections.keys()):
            if self.active_connections[key] == websocket:
                del self.active_connections[key]

    async def send_personal_message(self, user_id: int, message: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)


manager = ConnectionManager()


@app.get("/{user_id}")
async def get(user_id: int):
    return HTMLResponse(get_html(user_id))


def is_authenticated(data, sender_id) -> bool:
    return data == sender_id


# TODO: change to token based auth

@app.websocket("/ws/{sender_id}-{receiver_id}")
async def dialogue(
    websocket: WebSocket,
    sender_id: int,
    receiver_id: int,
):
    await manager.connect(sender_id, websocket)
    try:
        auth_data = await websocket.receive_text()

        if not is_authenticated(int(auth_data), sender_id):
            logger.info(f"User {auth_data} did not pass authentication to enter chat {sender_id}-{receiver_id}")
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

        while True:
            data = await websocket.receive_text()

            # TODO: Store message in storage
            await manager.send_personal_message(sender_id, data)
            await manager.send_personal_message(receiver_id, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        msg = f"{sender_id} has disconnected"
        await manager.send_personal_message(receiver_id, msg)
    except WebSocketException:
        manager.disconnect(websocket)
