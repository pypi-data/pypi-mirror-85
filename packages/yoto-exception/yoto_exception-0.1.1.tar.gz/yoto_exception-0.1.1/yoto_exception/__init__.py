import traceback
import logging
from typing import Union, Callable

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from yoto_exception.custom_exc import PostParamsError, TokenAuthError, YotoPermissionError
from yoto_exception.auth import AuthException
from yoto_exception.connection import ConnectionException
from yoto_exception.forbidden import ForbiddenException
from yoto_exception.maximum import MaximumException
from yoto_exception.permission import PermissionException
from yoto_exception.unknown import UnknownException


API_EXCEPTION_TUPLE = (
    AuthException,
    ConnectionException,
    ForbiddenException,
    MaximumException,
    PermissionException,
    UnknownException,
)


def register_exception(app: FastAPI, logger: logging.Logger, alarm: Callable):
    """
    全局异常捕获
    :param app:
    :param logger:
    :param alarm:
    :return:
    """

    # 捕获自定义异常
    @app.exception_handler(PostParamsError)
    async def query_params_exception_handler(request: Request, exc: PostParamsError):
        """
        捕获 自定义抛出的异常
        :param request:
        :param exc:
        :return:
        """
        err = f"参数查询异常\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
        logger.error(err)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"code": 400, "data": {"tip": exc.err_desc}, "message": "fail"},
        )

    @app.exception_handler(TokenAuthError)
    async def token_exception_handler(request: Request, exc: TokenAuthError):
        err = f"参数查询异常\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
        logger.error(err)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"code": 400, "data": None, "message": exc.err_desc},
        )

    @app.exception_handler(YotoPermissionError)
    async def permission_exception_handler(request: Request, exc: TokenAuthError):
        err = f"用户没有权限\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
        logger.error(err)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"code": 400, "data": None, "message": exc.err_desc},
        )

    # 捕获参数 验证错误
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """
        捕获请求参数 验证错误
        :param request:
        :param exc:
        :return:
        """
        err = f"参数错误\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
        logger.error(err)
        msg = {
            "code": 400,
            "data": {"tip": exc.errors()},
            "body": exc.body,
            "message": "fail",
        }
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(msg),
        )

    async def api_exception_handler(
        request: Request,
        exc: Union[
            AuthException,
            ConnectionException,
            ForbiddenException,
            MaximumException,
            PermissionException,
            UnknownException,
        ],
    ):
        err = f"未知实体异常\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
        logger.error(err)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"code": exc.code, "data": {}, "message": exc.err_desc},
        )

    # 捕获未知实体异常
    @app.exception_handler(UnknownException)
    async def unknown_exception_handler(request: Request, exc: UnknownException):
        return await api_exception_handler(request, exc)

    # 捕获权限异常
    @app.exception_handler(AuthException)
    async def auth_exception_handler(request: Request, exc: AuthException):
        return await api_exception_handler(request, exc)

    # 捕获连接请求异常
    @app.exception_handler(ConnectionException)
    async def connection_exception_handler(request: Request, exc: ConnectionException):
        return await api_exception_handler(request, exc)

    # 捕获禁止异常
    @app.exception_handler(ForbiddenException)
    async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
        return await api_exception_handler(request, exc)

    # 捕获超过数量上限异常
    @app.exception_handler(MaximumException)
    async def maximum_exception_handler(request: Request, exc: MaximumException):
        return await api_exception_handler(request, exc)

    # 捕获允许异常
    @app.exception_handler(PermissionException)
    async def api_permission_exception_handler(
        request: Request, exc: PermissionException
    ):
        return await api_exception_handler(request, exc)

    async def gene_exception_response(request: Request, errmsg: str) -> JSONResponse:
        err = f"全局异常\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}"
        logger.error(err)
        await alarm(err)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "data": {"tip": errmsg}, "message": "fail"},
        )

    # 捕获AssertionError异常
    @app.exception_handler(AssertionError)
    async def assert_error_handler(request: Request, exc: AssertionError):
        if exc.args and isinstance(exc.args[0], API_EXCEPTION_TUPLE):
            return await api_exception_handler(request, exc.args[0])

        return await gene_exception_response(request, f"{exc}")

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        return await gene_exception_response(request, "服务器错误")
