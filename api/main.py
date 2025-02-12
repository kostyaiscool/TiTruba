from fastapi import FastAPI
from endpoints import videos
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from db.session import init_database
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("start app")
    await init_database()
    yield
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

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)