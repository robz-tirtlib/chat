from uuid import UUID

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.message import DialogueMessageDTO
from src.application.dto.dialogue import DialogueParticipants
from src.application.interfaces.persistence.dialogue_repo import IDialogueRepo

from src.infrastructure.db.models.dialogue import Dialogue


class DialogueRepo(IDialogueRepo):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_dialogue(self, user1_id: UUID, user2_id: UUID) -> UUID:
        # what if we create already existing dialogue?
        stmnt = insert(Dialogue).values(
            user1_id=user1_id, user2_id=user2_id).returning(Dialogue.id)

        res = await self._session.execute(stmnt)
        return res.scalar()

    async def add_message(
            self, dialogue_id: UUID, sender_id: UUID, message_text: str,
    ) -> UUID:
        return await super().add_message(dialogue_id, sender_id, message_text)

    async def get_participants(
            self, dialogue_id: UUID,
    ) -> DialogueParticipants:
        return await super().get_participants(dialogue_id)

    async def get_message(self, message_id: UUID) -> DialogueMessageDTO:
        return await super().get_message(message_id)
