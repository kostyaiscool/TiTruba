from fastapi_users import FastAPIUsers

from modules.auth.backend import auth_backend
from modules.auth.dependencies.user_manager import get_user_manager
from modules.auth.models.user import User

# from auth.backend import auth_backend
# from auth.dependencies.user_manager import get_user_manager
# from auth.models.user import User

fastapi_users_routers = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_active_user = fastapi_users_routers.current_user(active=True)