from typing import Annotated

import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi import Depends, WebSocketException, status

from src.infrastructure.connection_manager import ConnectionManager

from src.presentation.api.templates.chat_page_generator import get_html
from src.presentation.api.dependencies.connection_manager import (
    get_connection_manager,
)


logger = logging.getLogger(__name__)

chat_router = APIRouter(prefix="/chats")


@chat_router.get("/{sender_id}-{receiver_id}")
async def get(sender_id: int, receiver_id: int):
    return HTMLResponse(get_html(sender_id, receiver_id))


def is_authenticated(data, sender_id) -> bool:
    return data == sender_id


# TODO: change to token based auth

@chat_router.websocket("/ws/{sender_id}-{receiver_id}")
async def dialogue(
    websocket: WebSocket,
    sender_id: int,
    receiver_id: int,
    manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
):
    await manager.connect(sender_id, websocket)
    try:
        auth_data = await websocket.receive_text()
        logger.info(f"auth_data={auth_data}")

        if not is_authenticated(int(auth_data), sender_id):
            logger.info(f"User {auth_data} did not pass authentication to \
                        enter chat {sender_id}-{receiver_id}")
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
