import logging

from typing import Annotated

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Depends

from src.application.commands.create_dialogue import CreateDialogueDTO
from src.application.commands.send_dialogue_message import \
    SendDialogueMessageDTO

from src.presentation.api.templates.chat_page_generator import get_html
from src.presentation.api.dependencies.stubs import get_user_by_token

from src.presentation.interactor_factory import InteractorFactory

from src.presentation.api.schemas.dialogue import (
    DialogueCreate, DialogueMessageCreate,
)


logger = logging.getLogger(__name__)

chat_router = APIRouter(prefix="/chats")


@chat_router.get("/{dialogue_id}")
async def get(dialogue_id: int):
    return HTMLResponse(get_html(dialogue_id))


@chat_router.post("/{dialogue_id}")
async def send_dialogue_message(
    data: DialogueMessageCreate, dialogue_id: int,  # TODO: change dialogue_id to UUID  # noqa
    ioc: Annotated[InteractorFactory, Depends()],
    user=Depends(get_user_by_token),
):
    async with ioc.send_dialogue_message() as _send_dialogue_message:
        message_id = await _send_dialogue_message(
            SendDialogueMessageDTO(
                dialogue_id=dialogue_id,
                sender_id=user.id,
                message_text=data.text,
            )
        )
        return {"message_id": message_id}


@chat_router.post("/")  # TODO: describe status codes responses
async def create_dialogue(
    data: DialogueCreate, ioc: Annotated[InteractorFactory, Depends()],
    user=Depends(get_user_by_token),
):
    async with ioc.create_dialogue() as _create_dialogue:
        dialogue_id = await _create_dialogue(
            CreateDialogueDTO(
                sender_id=user.id,
                receiver_id=data.user2_id,
            )
        )
        return {"dialogue_id": dialogue_id}
