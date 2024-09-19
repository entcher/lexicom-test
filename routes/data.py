from typing import Annotated
from schemas.data import Data, DataAddressOut
from fastapi import APIRouter, Depends, HTTPException

from database.config import RedisClient
from redis import Redis

router = APIRouter(tags=['data'])


async def get_address_by_phone_or_404(phone: str | int, cache: Redis):
    addressDB = await cache.get(phone)
    if addressDB is None:
        raise HTTPException(status_code=404, detail='Phone number not found')
    return addressDB


@router.get('/check_data', response_model=DataAddressOut)
async def get_address_by_phone(
    phone: str | int, cache: Annotated[(Redis, Depends(RedisClient.get_redis))]
):
    addressDB = await get_address_by_phone_or_404(phone, cache)
    return DataAddressOut(address=addressDB)


@router.post('/write_data', response_model=Data, status_code=201)
async def create_data(data: Data, cache: Annotated[(Redis, Depends(RedisClient.get_redis))]):
    addressDB = await cache.get(data.phone)
    if addressDB is not None:
        raise HTTPException(status_code=400, detail='Phone number already exists')

    await cache.set(data.phone, data.address)
    return data


@router.patch('/write_data', status_code=204)
async def update_data(data: Data, cache: Annotated[(Redis, Depends(RedisClient.get_redis))]):
    await get_address_by_phone_or_404(data.phone, cache)
    await cache.set(data.phone, data.address)
