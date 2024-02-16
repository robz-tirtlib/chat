from dataclasses import dataclass

from src.application.interfaces.persistence.dialogue_repo import IDialogueRepo


@dataclass
class CreateDialogueDTO:
    sender_id: str
    receiver_id: str


class CreateDialogue:
    def __init__(self, dialogue_repo: IDialogueRepo) -> None:
        self._dialogue_repo = dialogue_repo

    async def __call__(self, data: CreateDialogueDTO) -> str:
        # TODO: Prolly add smth like user privacy settings to restrict
        # dialogue creation

        dialogue_id = await self._dialogue_repo.add_dialogue(
            data.sender_id, data.receiver_id,
        )

        return dialogue_id
