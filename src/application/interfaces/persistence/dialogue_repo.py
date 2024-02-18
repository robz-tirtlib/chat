from abc import ABC, abstractmethod

from uuid import UUID

from src.application.dto.message import DialogueMessageDTO
from src.application.dto.dialogue import DialogueParticipants


class IDialogueRepo(ABC):
    @abstractmethod
    async def add_dialogue(self, user1_id: UUID, user2_id: UUID) -> int:
        ...

    @abstractmethod
    async def add_message(
            self, dialogue_id: int, sender_id: UUID, message_text: str,
    ) -> int:
        ...

    @abstractmethod
    async def get_participants(
            self, dialogue_id: int,
    ) -> DialogueParticipants:
        ...

    @abstractmethod
    async def get_message(self, message_id: int) -> DialogueMessageDTO:
        ...
