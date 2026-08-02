from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.users import UserCRUD
from models.subscribers import Subscriber
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

# @router.post("/subscribe/{user2}")
# async def subscribe(
#     user2: str,
#     db: AsyncSession = Depends(
#         db_helper.session_getter
#     ),
#     user: UserRead = Depends(
#         current_active_user
#     )
# ):
#     user_subscribed_to = (
#         await UserCRUD.get_user_by_name(
#             db,
#             user2
#         )
#     )
#     if user.id == user_subscribed_to.id:
#         return False
#
#     return await SubscriberCRUD.subscribe(
#         db,
#         user.id,
#         user_subscribed_to.id
#     )

@router.get("/get_username_by_id")
async def get_username_by_id(user_id: int):
    pass

@router.post("/subscribe/{user2}")
async def subscribe(
    user2: str,
    db: AsyncSession = Depends(db_helper.session_getter),
    user: UserRead = Depends(current_active_user),
):
    user_subscribed_to = await UserCRUD.get_user_by_name(
        db,
        user2,
    )

    if user.id == user_subscribed_to.id:
        return {
            "subscribed": False
        }

    return await SubscriberCRUD.toggle_subscribe(
        db,
        user.id,
        user_subscribed_to.id,
    )

@router.get("/status/{user2}")
async def status(
    user2: str,
    db: AsyncSession = Depends(db_helper.session_getter),
    user: UserRead = Depends(current_active_user),
):
    user2 = await UserCRUD.get_user_by_name(db, user2)

    subscription = await db.scalar(
        select(Subscriber).where(
            Subscriber.subscriber_id == user.id,
            Subscriber.subscribed_to_id == user2.id,
        )
    )

    return {
        "subscribed": subscription is not None
    }