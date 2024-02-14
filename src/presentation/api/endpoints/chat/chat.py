import logging

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi import Depends, WebSocketException, status

from src.infrastructure.db.models.dialogue import Dialogue
from src.infrastructure.connection_manager import ConnectionManager

from src.presentation.api.templates.chat_page_generator import get_html
from src.presentation.api.dependencies.stubs import (
    get_connection_manager, get_user_by_token, get_session_stub,
)


logger = logging.getLogger(__name__)

chat_router = APIRouter(prefix="/chats")


@chat_router.get("/{dialogue_id}")
async def get(dialogue_id: int):
    return HTMLResponse(get_html(dialogue_id))


# FIXME ?: resource id in ws route does not really make sense cuz
# we can send it in payload. But is it actually bad to have resource id in route?
# @chat_router.websocket("/ws/{dialogue_id}")
# async def dialogue(
#     websocket: WebSocket,
#     dialogue_id: int,
#     manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
#     session: Annotated[AsyncSession, Depends(get_session_stub)],
#     user=Depends(get_user_by_token),
# ):
#     from sqlalchemy import select, or_
#     smnt = select(Dialogue).where(
#         or_(
#             Dialogue.user1_id == user.id,
#             Dialogue.user2_id == user.id
#             )
#         )
#     dialogue = await session.execute(smnt)
#     dialogue.scalar()

#     if dialogue is None:
#         raise WebSocketException("No acces to dialogue.")
#     print(dialogue)

    # await manager.connect(user.id, websocket)

    # try:
    #     while True:
    #         data = await websocket.receive_text()

    #         # TODO: Store message in storage
    #         await manager.send_personal_message(sender_id, data)
    #         await manager.send_personal_message(receiver_id, data)
    # except WebSocketDisconnect:
    #     manager.disconnect(websocket)
    #     msg = f"{sender_id} has disconnected"
    #     await manager.send_personal_message(receiver_id, msg)
    # except WebSocketException:
    #     manager.disconnect(websocket)
