import uuid

import os

from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from src.infrastructure.db.models.user import User

from src.presentation.api.dependencies.stubs import get_user_db_stub


# TODO: refac UserManager (DI secrets; methods logic)
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = os.getenv("auth_secret")  # refac
    verification_token_secret = os.getenv("auth_secret")  # refac

    async def on_after_register(
            self, user: User, request: Optional[Request] = None,
    ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification req for user {user.id}. Verify token: {token}")


async def get_user_manager(user_db=Depends(get_user_db_stub)):
    yield UserManager(user_db)
