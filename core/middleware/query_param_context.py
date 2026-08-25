
from contextvars import ContextVar

from starlette.requests import Request

_request_ctx: ContextVar[Request] = ContextVar("request_ctx")


class RequestContext:

    @staticmethod
    def set_request(request: Request) -> None:
        """设置当前请求上下文"""
        _request_ctx.set(request)

    @staticmethod
    def get_request() -> Request:
        """获取当前请求上下文"""
        return _request_ctx.get()