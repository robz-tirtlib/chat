import logging

import uvicorn
import asyncio

from fastapi import FastAPI

from src.infrastructure.connection_manager import ConnectionManager

from src.presentation.api.endpoints.chat.chat import chat_router
from src.presentation.api.dependencies.connection_manager import (
    get_connection_manager,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(chat_router)

    def singleton_conn_manager(conn_manager):
        def factory():
            return conn_manager
        return factory

    connection_manager = ConnectionManager()

    app.dependency_overrides.update(
        {
            get_connection_manager: singleton_conn_manager(connection_manager),
        }
    )

    return app


async def run_api() -> None:
    app = create_app()

    # TODO: load config data (host, port etc.) from file/env
    config = uvicorn.Config(
        app=app,
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_api())
