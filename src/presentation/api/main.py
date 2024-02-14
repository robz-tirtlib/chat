import asyncio
import logging
import uvicorn
import uuid

from fastapi import FastAPI

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import AuthenticationBackend

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from dotenv import load_dotenv

from src.infrastructure.user_manager import get_user_manager
from src.infrastructure.connection_manager import ConnectionManager
from src.infrastructure.db.models.user import User
from src.infrastructure.db.config import load_db_config
from src.infrastructure.db.main import (
    get_engine, get_session_factory, get_user_db, get_database_strategy,
)

# TODO: all dependencies in one module
from src.presentation.api.endpoints.chat.chat import chat_router
from src.presentation.api.dependencies.stubs import (
    get_session_stub, get_user_db_stub, get_connection_manager,
    get_user_by_token, get_user_by_token_ws,
)
from src.presentation.api.schemas.user import UserCreate, UserRead

from src.presentation.api.utils import (
    get_user_from_cookie, get_user_from_cookie_ws,
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

    # TODO: stub other deps to override in tests
    app.dependency_overrides.update(
        {
            get_connection_manager: singleton_conn_manager(connection_manager),
            get_session_stub: get_session,
            get_user_db_stub: get_user_db,
            get_user_by_token_ws: get_user_from_cookie_ws,
            get_user_by_token: get_user_from_cookie,
        }
    )


def configure_auth(app: FastAPI):
    cookie_transport = CookieTransport()  # It's prolly also worth it to impl CORS and Origin check in white list, but I'll leave it for now  # noqa
    auth_backend = AuthenticationBackend(
        name="cookie",
        transport=cookie_transport,
        get_strategy=get_database_strategy,
    )

    fastapi_users = FastAPIUsers[User, uuid.UUID](
        get_user_manager,
        [auth_backend],
    )

    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/cookie",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"]
    )


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(chat_router)

    return app


# TODO: a bit messy here
async def run_api() -> None:
    app = create_app()
    await setup_dependencies(app)
    configure_auth(app)

    # TODO: load config data (host, port etc.) from file/env
    config = uvicorn.Config(
        app=app,
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_api())
