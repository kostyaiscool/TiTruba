from fastapi import FastAPI
from endpoints import videos

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
    return {'Ключик': 'IShowSpeed это н'}