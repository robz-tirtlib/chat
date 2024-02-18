from pydantic import BaseModel

from uuid import UUID


class DialogueCreate(BaseModel):
    user2_id: UUID


class DialogueMessageCreate(BaseModel):
    text: str
