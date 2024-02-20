import logging

from fastapi import WebSocket


logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self._conns: dict[int, WebSocket] = {}

    async def connect(self, client_id: int, websocket: WebSocket):
        await websocket.accept()
        self._conns[client_id] = websocket

    def disconnect(self, websocket: WebSocket):
        for key in list(self._conns.keys()):
            if self._conns[key] == websocket:
                del self._conns[key]
                return
        logger.warning(f"Websocket {websocket} is already disconnected.")

    async def send_personal_message(self, user_id: int, message: str):
        if user_id in self._conns:
            await self._conns[user_id].send_text(message)
