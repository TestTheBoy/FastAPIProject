# 创建上下文变量
from contextvars import ContextVar
from typing import Optional

current_query_param_ctx: ContextVar[Optional[dict]] = ContextVar("current_query_param", default=None)


class QueryParamContext:
    """
    查询参数上下文
    """

    @staticmethod
    def set_query_param(param: dict):
        """设置查询参数到上下文"""
        current_query_param_ctx.set(param)

    @staticmethod
    def get_query_param() -> dict:
        """从上下文获取当前用户"""
        return current_query_param_ctx.get() or {}
    
    @staticmethod
    def get_current_query_param() -> dict:
        """从上下文获取当前查询参数"""
        return QueryParamContext.get_query_param()

    @staticmethod
    def get_current_query_params() -> dict:
        """从上下文获取当前查询参数（别名）"""
        return QueryParamContext.get_query_param()