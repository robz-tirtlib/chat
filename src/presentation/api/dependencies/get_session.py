from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession


def get_session_stub() -> AsyncGenerator[AsyncSession, None]:
    raise NotImplementedError
