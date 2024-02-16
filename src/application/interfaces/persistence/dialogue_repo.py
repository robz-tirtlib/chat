from abc import ABC, abstractmethod


class IDialogueRepo(ABC):
    @abstractmethod
    async def add_dialogue(self, user1_id: str, user2_id: str) -> str:
        ...

    @abstractmethod
    async def add_message(
            self, dialogue_id: str, sender_id: str, message_text: str,
    ) -> str:
        ...
