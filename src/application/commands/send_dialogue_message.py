# Interactor
# No Depends (to easily test). Just construct Interactor manually in
# controller (request session or/and repo via Depends and inject them)

from dataclasses import dataclass

from uuid import UUID

from src.application.interfaces.persistence.dialogue_repo import IDialogueRepo


@dataclass
class SendDialogueMessageDTO:
    dialogue_id: int
    sender_id: UUID
    message_text: str


class SendDialogueMessage:
    def __init__(self, dialogue_repo: IDialogueRepo) -> None:
        self._dialogue_repo = dialogue_repo

    async def __call__(self, data: SendDialogueMessageDTO) -> int:
        # TODO: Prolly add smth like user privacy settings to restrict
        # message sending

        message_id = await self._dialogue_repo.add_message(
            data.dialogue_id, data.sender_id, data.message_text,
        )

        await self._dialogue_repo.commit()

        return message_id
