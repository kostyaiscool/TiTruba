from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase, DatabaseStrategy,
)

from modules.auth.dependencies.access_token import get_access_token_db
from modules.core.configs import settings

# from api.auth.dependencies.access_token import get_access_token_db
# from core.configs import settings

if TYPE_CHECKING:
    from api.modules.auth.models.access_token import AccessToken

def get_database_strategy(
    access_token_db: AccessTokenDatabase["AccessToken"] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db,
        lifetime_seconds=settings.auth.lifetime_seconds
    )