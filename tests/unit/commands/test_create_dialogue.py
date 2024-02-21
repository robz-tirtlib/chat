import pytest

from uuid import uuid4

from src.application.commands.create_dialogue import (
    CreateDialogue, CreateDialogueDTO,
)

from tests.mocks.dialogue_repo import DialogueRepoMock


@pytest.mark.asyncio
async def test_create_dialogue(dialogue_repo: DialogueRepoMock):
    command = CreateDialogue(dialogue_repo)
    res = await command(CreateDialogueDTO(
        sender_id=uuid4(),
        receiver_id=uuid4(),
    ))

    assert isinstance(res, int)

# TODO: test when dialogue already exists
