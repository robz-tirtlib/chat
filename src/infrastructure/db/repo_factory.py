from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.persistence.dialogue_repo import IDialogueRepo

from src.infrastructure.repos.dialogue import DialogueRepo


def get_dialogue_repo(session: AsyncSession) -> IDialogueRepo:
    return DialogueRepo(session)
