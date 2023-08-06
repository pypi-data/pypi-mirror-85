"""
    参数异常返回封装
"""
from typing import Union
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from fastapi import Request, status
from fastapi.responses import JSONResponse


async def http422_error_handler(_: Request, exc: Union[RequestValidationError, ValidationError],) -> JSONResponse:
    return JSONResponse(
        {
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "参数校验错误",
            "data": exc.errors(),
        },
        # status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        status_code=200,
    )
