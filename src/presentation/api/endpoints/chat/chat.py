from typing import Annotated

import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi import Depends, WebSocketException, status

from src.presentation.api.templates.chat_page_generator import get_html


logger = logging.getLogger(__name__)

chat_router = APIRouter(prefix="/chats")


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


@chat_router.get("/{user_id}")
async def get(user_id: int):
    return HTMLResponse(get_html(user_id))


def is_authenticated(data, sender_id) -> bool:
    return data == sender_id


# TODO: change to token based auth

@chat_router.websocket("/ws/{sender_id}-{receiver_id}")
async def dialogue(
    websocket: WebSocket,
    sender_id: int,
    receiver_id: int,
):
    await manager.connect(sender_id, websocket)
    try:
        auth_data = await websocket.receive_text()
        logger.info(f"auth_data={auth_data}")

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
