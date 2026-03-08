import asyncio

from fastapi import FastAPI

from core.configs import settings
from db.session import db_helper
from endpoints import videos
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

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