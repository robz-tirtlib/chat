from collections.abc import AsyncGenerator

from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
)
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase, DatabaseStrategy,
)

from fastapi import Depends

from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine,
)

from src.infrastructure.db.models import User
from src.infrastructure.db.config import DBConfig
from src.infrastructure.db.models.access_token import AccessToken

from src.presentation.api.dependencies.stubs import get_session_stub


async def get_engine(db_config: DBConfig) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        db_config.full_url,
        echo=True,
        echo_pool=db_config.echo,
        pool_size=50,
    )
    yield engine

    await engine.dispose()


def get_session_factory(
        engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(
        bind=engine, autoflush=False, expire_on_commit=False)
    return session_factory


async def get_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_session_stub)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_access_token_db(
    session: AsyncSession = Depends(get_session_stub),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


# FIXME: this is prolly not supposed to be here in db module
# since it is related to access. But I wont bother thinking about this
# right now.
def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),  # noqa
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db)
