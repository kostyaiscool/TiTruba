import asyncio

from fastapi import FastAPI

# from auth.routers.endpoints import auth_router
# from core.configs import settings
from db.session import db_helper
from endpoints import videos, users, subscribers, history
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from modules.auth.routers.endpoints import auth_router
from modules.core.configs import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("start app")
    await db_helper.init_db()
    yield
    await db_helper.dispose()
    print("end app")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники (лучше указать конкретный)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videos.router, prefix='/videos')
app.include_router(auth_router, prefix="/auth")
app.include_router(users.router)
app.include_router(subscribers.router, prefix='/subscribers')
app.include_router(history.router, prefix='/history')
@app.get('/')
async def home():
    return {'Ключик': 'IShowSpeed - Лучший стример'}

async def main():
    config = uvicorn.Config(
        app=app,
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())