"""
全局异常处理
"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("app.exceptions")


# ── 自定义业务异常 ──────────────────────────────────────────


class AppException(Exception):
    """应用基础异常"""

    def __init__(self, status_code: int = 500, detail: str = "服务器内部错误"):
        self.status_code = status_code
        self.detail = detail


class NotFoundError(AppException):
    def __init__(self, resource: str = "资源"):
        super().__init__(status_code=404, detail=f"{resource}未找到")


class ConflictError(AppException):
    def __init__(self, detail: str = "资源冲突"):
        super().__init__(status_code=409, detail=detail)


class BadRequestError(AppException):
    def __init__(self, detail: str = "请求参数错误"):
        super().__init__(status_code=400, detail=detail)


class UnauthorizedError(AppException):
    def __init__(self, detail: str = "未授权"):
        super().__init__(status_code=401, detail=detail)


# ── 全局异常处理器注册 ──────────────────────────────────────


def register_exception_handlers(app: FastAPI) -> None:
    """注册全局异常处理器"""

    @app.exception_handler(AppException)
    async def app_exception_handler(
        _request: Request, exc: AppException
    ) -> JSONResponse:
        logger.warning("AppException: %s (status=%d)", exc.detail, exc.status_code)
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        _request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "服务器内部错误"},
        )
