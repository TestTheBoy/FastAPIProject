from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from App_Demo.low_code_util import LowCodeUtil
from App_Demo.query_param_context import QueryParamContext
from core.middleware.query_param_context import RequestContext

class QueryParamMiddleware(BaseHTTPMiddleware):
    '''
        查询参数上下文中间件，主要用来设置查询参数
        '''
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        #设置请求上下文
        RequestContext.set_current_request(request)
        #获取原始请求体用于动态查询
        if request.method == "POST":
            try:
                body_bytes = await request.body()
                QueryParamContext.set_current_query_param(LowCodeUtil.get_query_param_map(body_bytes))
            except Exception as e:
                print(e)
            response = await call_next(request)
            return response
        return await call_next(request)