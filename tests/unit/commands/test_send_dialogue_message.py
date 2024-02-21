import pytest

from uuid import uuid4

from src.application.commands.create_dialogue import (
    CreateDialogue, CreateDialogueDTO,
)
from src.application.commands.send_dialogue_message import (
    SendDialogueMessage, SendDialogueMessageDTO,
)

from tests.mocks.dialogue_repo import DialogueRepoMock


@pytest.mark.asyncio
async def test_send_dialogue_message(dialogue_repo: DialogueRepoMock):
    command = CreateDialogue(dialogue_repo)
    sender = uuid4()
    dialogue_id = await command(CreateDialogueDTO(
        sender_id=sender,
        receiver_id=uuid4(),
    ))

    command = SendDialogueMessage(dialogue_repo)
    text = "Hi"
    msg_id = await command(SendDialogueMessageDTO(
        dialogue_id=dialogue_id,
        sender_id=sender,
        message_text=text,
    ))

    msg = await dialogue_repo.get_message(msg_id)
    assert msg.message_text == text


# TODO: test send to non-existent dialogue
# TODO: test send when no rights
