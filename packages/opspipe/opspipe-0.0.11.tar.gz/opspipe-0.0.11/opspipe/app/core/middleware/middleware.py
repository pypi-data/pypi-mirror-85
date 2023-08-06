"""中间件"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from ...settings.config import CORS_ORIGINS, CORS_ALLOW_METHODS, CORS_ALLOW_CREDENTIALS, CORS_ALLOW_HEADERS
import time


def init_middlewares(app: FastAPI):
    """初始化中间件"""
    app.state.log.info('init_middlewares ...')

    # cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=CORS_ALLOW_CREDENTIALS,
        allow_methods=CORS_ALLOW_METHODS,
        allow_headers=CORS_ALLOW_HEADERS,
    )

    # 中间件
    #@app.middleware("http")
    async def test(request: Request, call_next):
        #app.state.log.info('中间件 ...')
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
