from fastapi_users import IntegerIDMixin, BaseUserManager

from modules.auth.models.user import User
from modules.core.configs import settings


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.auth.reset_password_token_secret
    verification_token_secret = settings.auth.verification_token_secret