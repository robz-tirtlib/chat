from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession


def get_session_stub() -> AsyncGenerator[AsyncSession, None]:
    raise NotImplementedError


def get_connection_manager():
    raise NotImplementedError


def get_user_by_token():
    raise NotImplementedError


def get_user_db_stub():
    raise NotImplementedError
