from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Likes
from models.vidosi import Vidos
from modules.auth.schemas.user import UserRead


class LikesCRUD:

    @staticmethod
    async def rate_video(
        db: AsyncSession,
        user_id: int,
        video_id: int,
        rating: bool,
    ):
        result = await db.execute(
            select(Likes).where(
                Likes.liker_id == user_id,
                Likes.video_id == video_id,
            )
        )

        existing = result.scalar_one_or_none()

        if existing:
            # нажал ту же кнопку повторно
            if existing.rating == rating:
                await db.delete(existing)
                await db.commit()

                return {
                    "status": "removed"
                }

            # меняем лайк <-> дизлайк
            existing.rating = rating

            await db.commit()
            await db.refresh(existing)

            return {
                "status": "updated"
            }

        new_like = Likes(
            liker_id=user_id,
            video_id=video_id,
            rating=rating,
        )

        db.add(new_like)

        await db.commit()
        await db.refresh(new_like)

        return {
            "status": "created"
        }

    @staticmethod
    async def get_rating(
        db: AsyncSession,
        video_id: int,
    ):
        result = await db.execute(
            select(Likes).where(
                Likes.video_id == video_id
            )
        )

        ratings = result.scalars().all()

        likes_count = sum(
            1 for x in ratings
            if x.rating is True
        )

        dislikes_count = sum(
            1 for x in ratings
            if x.rating is False
        )

        return {
            "likes": likes_count,
            "dislikes": dislikes_count,
        }

    @staticmethod
    async def get_likes_logged(
            db: AsyncSession,
            user: UserRead,
    ):
        result = await db.execute(
            select(Vidos)
            .join(Likes, Likes.video_id == Vidos.id)
            .where(
                Likes.liker_id == user.id,
                Likes.rating == True
            )
        )

        videos = result.scalars().all()

        print(videos)

        return videos

    @staticmethod
    async def get_dislikes_logged(
            db: AsyncSession,
            user: UserRead,
    ):
        result = await db.execute(
            select(Vidos)
            .join(Likes, Likes.video_id == Vidos.id)
            .where(
                Likes.liker_id == user.id,
                Likes.rating == False
            )
        )

        videos = result.scalars().all()

        print(videos)

        return videos