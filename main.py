from fastapi import FastAPI
from api.endpoints import videos

app = FastAPI()
app.include_router(videos.router, prefix='/videos')
@app.get('/')
async def home():
    return {'Ключик': 'IShowSpeed это н'}