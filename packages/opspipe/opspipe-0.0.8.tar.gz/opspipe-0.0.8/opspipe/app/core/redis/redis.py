"""
初始化redis
"""
from fastapi import FastAPI
from aioredis import create_redis_pool, Redis
from ...settings.config import REDIS_HOST, REDIS_PORT, REDIS_DB,REDIS_INIT


async def redis_init(app: FastAPI) -> Redis:
    # Redis.
    # redis_pool = await create_redis_pool(f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?encoding=utf-8")
    if REDIS_INIT :
        redis_pool = await create_redis_pool(address=f"redis://{REDIS_HOST}:{REDIS_PORT}", db=REDIS_DB, encoding='utf-8')
        app.state.log.info('redis_init ...')
        return redis_pool
    else:
        return None
