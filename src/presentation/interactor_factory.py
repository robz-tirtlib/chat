from abc import ABC, abstractmethod

from src.application.commands.create_dialogue import CreateDialogue


class InteractorFactory(ABC):

    @abstractmethod
    async def create_dialogue(self) -> CreateDialogue:
        ...
