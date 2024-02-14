from fastapi import Depends, WebSocket

from websockets import WebSocketException

from src.infrastructure.user_manager import get_user_manager
from src.infrastructure.db.main import get_database_strategy


async def get_user_from_cookie(
    websocket: WebSocket,
    strategy=Depends(get_database_strategy),
    user_manager=Depends(get_user_manager),
):
    cookie = websocket.cookies.get("fastapiusersauth")
    user = await strategy.read_token(cookie, user_manager)
    if not user or not user.is_active:
        raise WebSocketException("Invalid user")
    yield user
