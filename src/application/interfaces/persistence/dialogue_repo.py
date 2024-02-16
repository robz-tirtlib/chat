from abc import ABC, abstractmethod

from uuid import UUID


class IDialogueRepo(ABC):
    @abstractmethod
    async def add_dialogue(self, user1_id: UUID, user2_id: UUID) -> UUID:
        ...

    @abstractmethod
    async def add_message(
            self, dialogue_id: UUID, sender_id: UUID, message_text: str,
    ) -> UUID:
        ...
