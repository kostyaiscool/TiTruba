from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from modules.auth.schemas.user import UserRead
from models.subscribers import Subscriber


class SubscriberCRUD():
    # @staticmethod
    # async def get_subscribers(session: AsyncSession, user: UserRead):
    #     subscribers = await session.execute(select(Subscriber).where(Subscriber.subscriber_id == user.id))
    #     return subscribers.scalars().all()
    @staticmethod
    async def get_subscribers(
            session: AsyncSession,
            user: UserRead,
    ):
        result = await session.execute(
            select(Subscriber)
            .options(
                selectinload(Subscriber.subscribed_to)
            )
            .where(
                Subscriber.subscriber_id == user.id
            )
        )

        subscribers = result.scalars().all()

        return [
            {
                "id": sub.id,
                "subscribed_to_id": sub.subscribed_to_id,
                "username": sub.subscribed_to.username,
            }
            for sub in subscribers
        ]

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

    @staticmethod
    async def toggle_subscribe(
            session: AsyncSession,
            subscriber_id: int,
            subscribed_to_id: int,
    ):
        subscription = await session.scalar(
            select(Subscriber).where(
                Subscriber.subscriber_id == subscriber_id,
                Subscriber.subscribed_to_id == subscribed_to_id,
            )
        )

        # Уже подписан → отписываемся
        if subscription:
            await session.delete(subscription)
            await session.commit()

            return {
                "subscribed": False
            }

        # Не подписан → подписываемся
        subscription = Subscriber(
            subscriber_id=subscriber_id,
            subscribed_to_id=subscribed_to_id,
        )

        session.add(subscription)

        await session.commit()

        return {
            "subscribed": True
        }