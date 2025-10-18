from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from api.core.configs import get_settings
from sqlalchemy.ext.declarative import declarative_base


class DatabaseManager():
    def __init__(self):
        self.settings = get_settings()
        self._engine: AsyncEngine = create_async_engine(self.settings.db.url, future=True, echo=True)
        self._session_factory = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

        Base = declarative_base()


async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# async def get_db():
#     async with session() as session:
#         yield session
