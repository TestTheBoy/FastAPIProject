from enum import Enum
from typing import List, Optional, Union
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from App_Demo.base import R
from App_Demo.user_context import UserContext
from App_Demo.util import JwtUtil, StrUtil
from modules.sys.services.auth_service import AuthService
# from modules.sys.services.auth_service import AuthService
from modules.sys.vos.auth_vo import LoginUser


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, while_list=[],
                 token_key="Authorization",
                 token_prefix="Bearer ",
                 ):
        super().__init__(app)
        self.while_list = while_list
        self.token_key = token_key
        self.token_prefix = token_prefix
        print(f"AuthMiddleware init{self.while_list}")

    async def dispatch(self, request, call_next):
        __sa_ignore__ = False
        # 遍历路由，找到当前请求对应的路由对象
        for route in request.app.routes:
            if route.path == request.url.path and request.method in route.methods:
                # 获取权限码
                if hasattr(route.endpoint, '__sa_ignore__'):
                    __sa_ignore__ = getattr(route.endpoint, '__sa_ignore__')
        # 白名单
        while_list_flag = False
        if self.while_list:
            for pattern in self.while_list:
                if StrUtil.ant_matcher(request.url.path, pattern):
                    while_list_flag = True
        if __sa_ignore__ or while_list_flag: return await call_next(request)
        authorization = request.headers.get(self.token_key)
        # 先获取token
        if authorization and authorization.startswith(self.token_prefix):
            authorization = authorization[7:]  # 去掉"Bearer "前缀
        # 验证token
        payload = JwtUtil.verify_token(authorization, AuthService.jwt_secret)
        # 校验不通过，返回错误信息
        if not payload: return JSONResponse(content=R.fail_with_code(99990403, "登录凭证已过期").model_dump())
        # 给当前请求设置用户ID
        UserContext.set_current_user(payload)
        # 校验权限码，默认规则为：/sys/user/page==>sys:user:page
        # permCode = request.url.path[1:].replace('/', ':')
        # if permCode not in payload.get('permCodes', []):
        #   return JSONResponse(content=R.fail_with_code(99990406, f"您没有访问{request.url.path}权限").model_dump())
        # 这里有获取到当前请求执行方法绑定的SaCheckPermission对象
        sa_check_permission: Union[SaCheckPermission, None] = None
        # 遍历路由，找到当前请求对应的路由对象
        for route in request.app.routes:
            if route.path == request.url.path and request.method in route.methods:
                # 获取权限码
                if hasattr(route.endpoint, '__sa_check_permission__'):
                    sa_check_permission = getattr(route.endpoint, '__sa_check_permission__')

        # if sa_check_permission:
        #     mode = sa_check_permission.mode or SaMode.AND
        #     permCodes = sa_check_permission.value
        #     print(f"mode:{mode}")
        #     print(f"permCode:{permCodes}")
        # else:
        #     print("没有权限检查")

        superAdmin = payload.superAdmin
        if not superAdmin and sa_check_permission:
            mode = sa_check_permission.mode or SaMode.AND
            permCodes: List[str] = sa_check_permission.value

            userPermCodes = payload.permCodes or []
            if mode == SaMode.AND:
                if not all(permCode in userPermCodes for permCode in permCodes):
                    return JSONResponse(
                        content=R.fail_with_code(99990406, f"您没有访问{request.url.path}权限").model_dump())
            elif mode == SaMode.OR:
                if not any(permCode in userPermCodes for permCode in permCodes):
                    return JSONResponse(
                        content=R.fail_with_code(99990406, f"您没有访问{request.url.path}权限").model_dump())
        else:
            print("没有权限检查")
            # 获取权限码
        # 校验通过，继续处理请求
        response = await call_next(request)
        return response


class SaMode(Enum):
    AND = "AND"
    OR = "OR"


class SaCheckPermission:
    """
    权限检查装饰器，用于限制访问特定接口
    仿照Java Sa-Token的@SaCheckPermission注解实现
    """

    def __init__(
            self,
            value: Optional[Union[str, List[str]]] = None,
            type: str = "",
            mode: SaMode = SaMode.AND,
            or_role: Optional[List[str]] = None
    ):
        """
        初始化权限检查装饰器

        :param value: 权限码，可以是字符串或字符串列表
        :param type: 权限类型
        :param mode: 权限检查模式（AND 或 OR）
        :param or_role: 角色列表，满足任一角色即可访问
        """
        self.type = type
        self.mode = mode
        self.or_role = or_role or []

        if value is None:
            self.value = []
        elif isinstance(value, str):
            self.value = [value]
        else:
            self.value = value

    def __call__(self, func):
        # 通过装饰器保存权限检查信息到函数属性
        func.__sa_check_permission__ = self
        return func



class SaIgnore:
    """
    忽略权限检查装饰器
    仿照Java Sa-Token的@SaIgnore注解实现
    """

    def __call__(self, func):
        # 标记函数为忽略权限检查
        func.__sa_ignore__ = True
        return func