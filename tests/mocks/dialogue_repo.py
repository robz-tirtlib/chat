from uuid import UUID
from src.application.dto.dialogue import DialogueParticipants
from src.application.dto.message import DialogueMessageDTO

from src.application.interfaces.persistence.dialogue_repo import IDialogueRepo


class DialogueRepoMock(IDialogueRepo):
    def __init__(self):
        self.dialogues: dict = {}
        self.dialogue_messages: dict = {}

        self.dialogue_id = 1
        self.message_id = 1

    async def add_dialogue(self, user1_id: UUID, user2_id: UUID) -> int:
        self.dialogues[self.dialogue_id] = {
            "user1_id": user1_id,
            "user2_id": user2_id,
        }
        self.dialogue_id += 1
        return self.dialogue_id - 1

    async def add_message(
            self, dialogue_id: int, sender_id: UUID, message_text: str) -> int:
        self.dialogue_messages[self.message_id] = {
            "dialogue_id": dialogue_id,
            "sender_id": sender_id,
            "text": message_text,
        }
        self.message_id += 1

        return self.message_id - 1

    async def get_participants(self, dialogue_id: int) -> DialogueParticipants:
        for d_id, d_vals in self.dialogues.items():
            if d_id == dialogue_id:
                return DialogueParticipants(
                    user1_id=d_vals["user1_id"],
                    user2_id=d_vals["user2_id"],
                )

    async def get_message(self, message_id: int) -> DialogueMessageDTO:
        msg = self.dialogue_messages[message_id]
        return DialogueMessageDTO(
            id=message_id,
            dialogue_id=msg["dialogue_id"],
            sender_id=msg["sender_id"],
            message_text=msg["text"],
        )

    async def commit(self) -> None:
        ...
