from abc import ABC, abstractmethod

from typing import AsyncIterator

from src.application.commands.create_dialogue import CreateDialogue
from src.application.commands.send_dialogue_message import SendDialogueMessage
from src.application.commands.notify_new_dialogue_message import \
    NotifyNewDialogueMessage
from src.application.interfaces.notifier import INotifier


class InteractorFactory(ABC):

    @abstractmethod
    async def create_dialogue(self) -> AsyncIterator[CreateDialogue]:
        ...

    @abstractmethod
    async def send_dialogue_message(
            self) -> AsyncIterator[SendDialogueMessage]:
        ...

    @abstractmethod
    async def notify_new_dialogue_message(
            self, notifier: INotifier,
    ) -> AsyncIterator[NotifyNewDialogueMessage]:
        ...
