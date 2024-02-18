from dataclasses import dataclass

from uuid import UUID


@dataclass
class DialogueMessageDTO:
    id: int
    dialogue_id: int
    sender_id: UUID
    message_text: str
