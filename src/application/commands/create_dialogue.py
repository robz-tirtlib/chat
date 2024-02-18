from dataclasses import dataclass

from uuid import UUID

from src.application.interfaces.persistence.dialogue_repo import IDialogueRepo


@dataclass
class CreateDialogueDTO:
    sender_id: UUID
    receiver_id: UUID


class CreateDialogue:
    def __init__(self, dialogue_repo: IDialogueRepo) -> None:
        self._dialogue_repo = dialogue_repo

    async def __call__(self, data: CreateDialogueDTO) -> int:
        # TODO: Prolly add smth like user privacy settings to restrict
        # dialogue creation

        # TODO: check if user with 'receiver_id' exists

        dialogue_id = await self._dialogue_repo.add_dialogue(
            data.sender_id, data.receiver_id,
        )

        return dialogue_id
