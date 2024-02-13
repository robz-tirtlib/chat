from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTableUUID,
)

from src.infrastructure.db.models.base import Base


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass
