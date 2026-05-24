from fastapi_users.authentication import AuthenticationBackend

from modules.auth.dependencies.strategy import get_database_strategy
from modules.auth.transport import bearer_transport

# from api.auth.dependencies.strategy import get_database_strategy
# from api.auth.transport import bearer_transport

auth_backend = AuthenticationBackend(
    name="access-token-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy
)