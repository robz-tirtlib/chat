import asyncio
import logging
import uvicorn

from fastapi import FastAPI

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from dotenv import load_dotenv

from src.infrastructure.connection_manager import ConnectionManager
from src.infrastructure.db.config import load_db_config
from src.infrastructure.db.main import get_engine, get_session_factory
from src.presentation.api.dependencies.get_session import get_session_stub

from src.presentation.api.endpoints.chat.chat import chat_router
from src.presentation.api.dependencies.connection_manager import (
    get_connection_manager,
)

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def setup_dependencies(app: FastAPI) -> None:
    db_config = load_db_config()
    engine = await anext(get_engine(db_config))
    session_factory = get_session_factory(engine)

    async def get_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    def singleton_conn_manager(conn_manager):
        def factory():
            return conn_manager
        return factory

    connection_manager = ConnectionManager()

    app.dependency_overrides.update(
        {
            get_connection_manager: singleton_conn_manager(connection_manager),
            get_session_stub: get_session,
        }
    )


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(chat_router)

    return app


async def run_api() -> None:
    app = create_app()
    await setup_dependencies(app)

    # TODO: load config data (host, port etc.) from file/env
    config = uvicorn.Config(
        app=app,
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_api())
