from dataclasses import dataclass

from uuid import UUID

from src.application.interfaces.persistence.dialogue_repo import IDialogueRepo
from src.application.interfaces.notifier import INotifier


@dataclass
class NotifyNewDialogueMessageDTO:
    dialogue_id: UUID
    message_id: UUID


class NotifyNewDialogueMessage:

    def __init__(
            self, dialogue_repo: IDialogueRepo, notifier: INotifier,
    ) -> None:
        self._dialogue_repo = dialogue_repo
        self._notifier = notifier

    async def __call__(self, data: NotifyNewDialogueMessageDTO) -> None:
        # TODO: what if there are less or more than 2 users?

        users = await self._dialogue_repo.get_participants(
            data.dialogue_id)

        message = await self._dialogue_repo.get_message(data.message_id)

        receiver_id = (users.user1_id if users.user2_id == message.sender_id
                       else users.user2_id)

        await self._notifier.notify_new_message(
            message.sender_id, receiver_id, data.message_id,
            message.message_text,
        )
