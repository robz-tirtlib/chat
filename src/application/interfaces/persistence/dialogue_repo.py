from abc import ABC, abstractmethod

from uuid import UUID

from src.application.dto.message import DialogueMessageDTO


class IDialogueRepo(ABC):
    @abstractmethod
    async def add_dialogue(self, user1_id: UUID, user2_id: UUID) -> UUID:
        ...

    @abstractmethod
    async def add_message(
            self, dialogue_id: UUID, sender_id: UUID, message_text: str,
    ) -> UUID:
        ...

    @abstractmethod
    async def get_participants(self, dialogue_id: UUID) -> list[UUID]:  # TODO: change output type # noqa
        ...

    @abstractmethod
    async def get_message(self, message_id: UUID) -> DialogueMessageDTO:
        ...
