from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from App_Demo.base import R
from core.exception import BizException, GlobalErrorEnum
from core.permission import NotLoginException, NotPermissionException, SaTokenException


def setup_exception_handlers(app: FastAPI):
    """设置全局异常处理器"""
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """处理请求验证错误"""
        errors = exc.errors()
        message = errors[0].get('msg', '请求参数验证失败')
        if 'loc' in errors[0]:
            field = errors[0]['loc'][-1] if errors[0]['loc'] else 'unknown'
            message = f"字段 '{field}' {message}"
        request.state.error_message = message
        return JSONResponse(
            status_code=200,
            headers={'success': 'N'},
            content=R.fail(msg=message, code=GlobalErrorEnum.GL99999999.code).model_dump()
        )

    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """处理 HTTP 异常"""
        request.state.error_message = exc.detail
        return JSONResponse(
            status_code=200,
            headers={'success': 'N'},
            content=R.fail(msg=exc.detail, code=exc.status_code).model_dump()
        )

    @app.exception_handler(NotLoginException)
    async def not_login_exception_handler(request: Request, exc: NotLoginException):
        """处理未登录异常"""
        message = getattr(exc, "message", None) or getattr(exc, "msg", None) or "未登录"
        request.state.error_message = message
        return JSONResponse(
            status_code=401,
            headers={'success': 'N'},
            content=R.fail(msg=message, code=GlobalErrorEnum.GL99990401.code).model_dump()
        )
    
    @app.exception_handler(NotPermissionException)
    async def not_permission_exception_handler(request: Request, exc: NotPermissionException):
        """处理无权限异常"""
        message = getattr(exc, "message", None) or getattr(exc, "msg", None) or "无权限"
        request.state.error_message = message
        return JSONResponse(
            status_code=403,
            headers={'success': 'N'},
            content=R.fail(msg=message, code=GlobalErrorEnum.GL99990403.code).model_dump()
        )
    @app.exception_handler(SaTokenException)
    async def sa_token_exception_handler(request: Request, exc: SaTokenException):
        """处理Sa-Token异常"""
        message = getattr(exc, "message", None) or getattr(exc, "msg", None) or "token异常"
        request.state.error_message = message
        return JSONResponse(
            status_code=401,
            headers={'success': 'N'},
            content=R.fail(msg=message, code=GlobalErrorEnum.GL99990401.code).model_dump()
        )
    @app.exception_handler(BizException)
    async def biz_exception_handler(request: Request, exc: BizException):
        """处理业务异常"""
        message = getattr(exc, "message", None) or getattr(exc, "msg", None) or "业务异常"
        request.state.error_message = message
        return JSONResponse(
            status_code=200,
            headers={'success': 'N'},
            content=R.fail(msg=message, code=exc.code).model_dump()
        )
    
   
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """处理通用异常"""
        request.state.error_message = str(exc) or '服务器内部错误'
        return JSONResponse(
            status_code=200,
            headers={'success': 'N'},
            content=R.fail(msg="服务器内部错误", code=GlobalErrorEnum.GL99990500.code).model_dump()
        )
    

    @app.exception_handler(404)
    async def general_404_exception_handler(request: Request, exc: Exception):
        """处理404异常"""
        request.state.error_message = str(exc) or '资源不存在'
        return JSONResponse(
            status_code=200,
            headers={'success': 'N'},
            content=R.fail(msg="此功能正在建设中，敬请期待！", code=GlobalErrorEnum.GL99990404.code).model_dump()
        )