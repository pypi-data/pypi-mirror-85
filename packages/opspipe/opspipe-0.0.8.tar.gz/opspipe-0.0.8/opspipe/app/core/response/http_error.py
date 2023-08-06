"""
错误异常
"""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from .BaseResponse import UnicornException


async def http_error_handler(_: Request, exc: HTTPException):
    if exc.status_code == 4000:
        return JSONResponse({
            "code": 4000,
            "message": exc.detail,
            "data": exc.detail
        })
    if exc.status_code == 4003:
        return JSONResponse({
            "code": 4003,
            "message": exc.detail,
            "data": exc.detail
        })
    return JSONResponse({
        "code": exc.status_code,
        "message": exc.detail,
        "data": exc.detail
    }, status_code=exc.status_code)


async def unicorn_exception_handler(_: Request, exc: UnicornException):
    return JSONResponse({
        "code": exc.code,
        "message": exc.errmsg,
        "data": exc.data,
    })

