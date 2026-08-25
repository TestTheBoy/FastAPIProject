from contextlib import asynccontextmanager
import json
import logging
import os
import time
from time import process_time

from database import SessionLocal, get_redis, init_db
import uvicorn

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_serializer
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from App_Demo.base import R
from App_Demo.exception_handler import setup_exception_handlers
from App_Demo.query_param_middleware import QueryParamContextMiddleware
from App_Demo.util import JwtUtil
from core.ioc_container import get_service, register
from core.redis_token_store import RedisTokenStore
from core.token_manager import TokenManager
from modules.sys.controllers.auth_controller import router as auth_router
from modules.sys.controllers.user_controllers import router as user_router
from modules.sys.controllers.role_controllers import router as role_router
from modules.sys.controllers.post_controller import router as post_router
from modules.sys.controllers.dept_controller import router as dept_router
from modules.sys.controllers.menu_controller import router as menu_router
from modules.sys.controllers.dict_item_controller import router as dect_item_router
from modules.sys.controllers.file_info_controller import router as file_info_router
from modules.sys.controllers.config_controller import router as config_router
from modules.sys.services.auth_service import AuthService
from App_Demo.auth_middleware import AuthMiddleware
from modules.sys.controllers.rbac_controller import router as rbac_router
from modules.sys.controllers.low_code_controller import router as low_code_router
from modules.sys.controllers.dict_controller import router as dict_router
from modules.sys.controllers.message_controller import router as message_router
from modules.sys.services.captcha_service import CaptchaCache, CaptchaService
from modules.sys.services.config_service import ConfigService

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

@asynccontextmanager
async def lifespans(app: FastAPI):
    # 启动阶段
    logging.info("应用启动中...")
    # 初始化数据库连接
    init_db(app)
    db: Session = SessionLocal()
    config_service: ConfigService = get_service("ConfigService", db=db)
    config_service.init_config_cache()
    logging.info("配置常量初始化完成")
    # 初始化 TokenManager 使用 Redis 存储
    TokenManager.init_store(RedisTokenStore(redis_client=get_redis()))
    logging.info("TokenManager 初始化完成")
    yield
    # 关闭阶段
    logging.info("应用关闭中...")
    db.close()

app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespans)
setup_exception_handlers(app)  # 设置全局异常处理

#注册
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(post_router)
app.include_router(dept_router)
app.include_router(config_router)
app.include_router(dect_item_router)
app.include_router(file_info_router)
app.include_router(dict_router)
app.include_router(menu_router)
app.include_router(rbac_router)
app.include_router(message_router)
app.add_middleware(AuthMiddleware,while_list=["/docs","/openapi.json","/static/**","/uploadfiles/**"],token_key="Authorization")

app.add_middleware(QueryParamContextMiddleware)
app.include_router(low_code_router)  #低代接口优先级较高，放在最后注册
#自定义Swagger UI路由，使用本地资源
@app.get("/docs",include_in_schema= False) #不显示在API文档中
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/favicon.ico",
    )

class CommonHeaders(BaseModel):
    host: str | None = Field(None, alias="Host")
    save_data: bool | None = Field(None, alias="Save-Data")
    if_modified_since: str | None = Field(None, alias="If-Modified-Since")
    traceparent: str | None = Field(None, alias="Traceparent")
    x_tag: list[str] | None = Field(None, alias="X-Tag")


#引入静态文件
app.mount("/static",StaticFiles(directory="static"),name="static")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploadfiles")
os.makedirs(UPLOAD_DIR, exist_ok=True)
#所有/uploadfiles开头的请求，都映射到项目内的 uploadfiles 目录下
app.mount("/uploadfiles", StaticFiles(directory=UPLOAD_DIR), name="uploadfiles")

# 创建并注册
captcha_cache = CaptchaCache()
register("CaptchaCache", captcha_cache)

captcha_service = CaptchaService()
register("CaptchaService", captcha_service)

# 注册 VisLogService（访问日志服务）
register("VisLogService", "modules.sys.services.vis_log_service", "VisLogService")


# WHILE_LIST = [
#     "/sys/login",
# ]

#中间件
# @app.middleware("auth")
# async def auth_handler(request: Request, call_next):
#     #白名单
#     if request.url.path in WHILE_LIST:
#         return await call_next(request)
#     authorization = request.headers.get("Authorization")
#     #先获取token
#     if authorization and authorization.startswith("Bearer "):
#         authorization = authorization[7:] # 去掉 Bearer 前缀
#     response = await call_next(request)
#     #验证token
#     payload = JwtUtil.verify_token(authorization, AuthService.jwt_secret)
#     #校验不通过返回错误信息
#     if not payload:return JSONResponse(content=R.fail_with_code(9999403, "登录凭证已过期").model_dump())
#     #校验通过，继续处理请求
#     response = await call_next(request)
#     return response

# 通配符路由处理所有未匹配的路径
# @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"], include_in_schema=False)
# async def catch_all():
#     return R.fail(msg="此功能正在建设中，敬请期待！", code=99990404)

if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
