import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from App_Demo.query_param_context import QueryParamContext
from core.middleware.query_param_context import RequestContext

class QueryParamContextMiddleware(BaseHTTPMiddleware):
    """
    查询参数上下文中间件，主要用于设置查询参数
    """
    async def dispatch(self, request: Request, call_next):
        # 设置请求上下文
        RequestContext.set_request(request)
        # 获取原始请求体用于动态查询
        if request.method == "POST":
          try:
            body_bytes = await request.body()
            QueryParamContext.set_query_param(json.loads(body_bytes))
          except Exception:
            pass
          response = await call_next(request)
          return response
        return await call_next(request)