from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from modules.auth.schemas.user import UserRead
from models.subscribers import Subscriber


class SubscriberCRUD():
    @staticmethod
    async def get_subscribers(session: AsyncSession, user: UserRead):
        subscribers = await session.execute(select(Subscriber).where(Subscriber.subscriber_id == user.id))
        return subscribers.scalars().all()

    @staticmethod
    async def subscribe(
            session: AsyncSession,
            subscriber_id: int,
            subscribed_to_id: int,
    ):
        subscription = Subscriber(
            subscriber_id=subscriber_id,
            subscribed_to_id=subscribed_to_id,
        )
        if subscriber_id != subscribed_to_id:
            session.add(subscription)

        await session.commit()
        await session.refresh(subscription)

        return subscription