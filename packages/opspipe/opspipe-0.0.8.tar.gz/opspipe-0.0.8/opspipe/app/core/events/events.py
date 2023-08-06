"""
事件监听
""" 
from typing import Callable
from fastapi import FastAPI
from ..redis.redis import redis_init  


# app 启动
def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None: 
        app.state.log.info('app_start....')
        # 补充APP启动时需要的动作，例如：链接数据库
        # Redis   
        app.state.Redis = await redis_init(app)
    return start_app


# app 停止
def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        app.state.log.info('app_stop ...')
        # 补充APP关闭时需要的动作：例如关闭数据库
        await app.state.Redis.closed()

    return stop_app
