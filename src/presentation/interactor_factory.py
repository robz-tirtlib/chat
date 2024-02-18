from abc import ABC, abstractmethod

from typing import AsyncIterator

from src.application.commands.create_dialogue import CreateDialogue
from src.application.commands.send_dialogue_message import SendDialogueMessage


class InteractorFactory(ABC):

    @abstractmethod
    async def create_dialogue(self) -> AsyncIterator[CreateDialogue]:
        ...

    @abstractmethod
    async def send_dialogue_message(
            self) -> AsyncIterator[SendDialogueMessage]:
        ...
