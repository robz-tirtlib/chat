from abc import ABC, abstractmethod

from uuid import UUID


class INotifier(ABC):

    @abstractmethod
    async def notify_new_message(
            self, sender_id: UUID, receiver_id: UUID, message_id: int,
            message_text: str,
    ) -> None:
        ...
