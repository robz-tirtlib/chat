from typing import AsyncIterator

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.commands.create_dialogue import CreateDialogue

from src.infrastructure.db.repo_factory import get_dialogue_repo

from src.presentation.interactor_factory import InteractorFactory


class IoC(InteractorFactory):

    def __init__(
            self, session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._session_factory = session_factory

    @asynccontextmanager
    async def create_dialogue(self) -> AsyncIterator[CreateDialogue]:
        async with self._session_factory() as session:
            dialogue_repo = get_dialogue_repo(session)
            yield CreateDialogue(dialogue_repo)
