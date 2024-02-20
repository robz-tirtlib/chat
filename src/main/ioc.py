from typing import AsyncIterator

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.commands.create_dialogue import CreateDialogue
from src.application.commands.notify_new_dialogue_message import \
    NotifyNewDialogueMessage
from src.application.commands.send_dialogue_message import SendDialogueMessage
from src.application.interfaces.notifier import INotifier

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

    @asynccontextmanager
    async def send_dialogue_message(
            self) -> AsyncIterator[SendDialogueMessage]:
        async with self._session_factory() as session:
            dialogue_repo = get_dialogue_repo(session)
            yield SendDialogueMessage(dialogue_repo)

    @asynccontextmanager
    async def notify_new_dialogue_message(
            self, notifier: INotifier,
    ) -> AsyncIterator[NotifyNewDialogueMessage]:
        async with self._session_factory() as session:
            dialogue_repo = get_dialogue_repo(session)
            yield NotifyNewDialogueMessage(dialogue_repo, notifier)
