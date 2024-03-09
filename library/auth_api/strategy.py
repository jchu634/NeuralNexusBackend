import uuid

from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy

from library.database.models import AccessToken, User
from library.database.database import get_access_token_db


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(
        get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)
