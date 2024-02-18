from dataclasses import dataclass

from uuid import UUID


@dataclass
class DialogueParticipants:
    user1_id: UUID
    user2_id: UUID
