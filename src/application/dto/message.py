from dataclasses import dataclass

from uuid import UUID


@dataclass
class DialogueMessageDTO:
    id: UUID
    dialogue_id: UUID
    sender_id: UUID
    message_text: str
