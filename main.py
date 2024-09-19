from contextlib import asynccontextmanager

from database.config import RedisClient
from routes.data import router as DataRouter

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):
    RedisClient.init()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(DataRouter)
