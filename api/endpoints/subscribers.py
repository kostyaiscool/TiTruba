from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.users import UserCRUD
from modules.auth.routers.fastapi_users_endpoints import current_active_user
from modules.auth.schemas.user import UserRead
from crud.subscribers import SubscriberCRUD
from db.session import db_helper

router = APIRouter()
@router.get("/get_subscribers")
async def get_subscribers(db: AsyncSession = Depends(db_helper.session_getter),
                          user: UserRead = Depends(current_active_user)):
    subscribers = await SubscriberCRUD.get_subscribers(db, user)
    return subscribers

@router.post("/subscribe/{user2}")
async def subscribe(user2: str, db: AsyncSession = Depends(db_helper.session_getter),
                    user: UserRead = Depends(current_active_user)):
    user_subscribed_to = await UserCRUD.get_user_by_name(db, user2)
    if user != user2:
        subscription = await SubscriberCRUD.subscribe(db, user.id, user_subscribed_to.id)
        return subscription
    else:
        return False

@router.get("/get_username_by_id")
async def get_username_by_id(user_id: int):
    pass