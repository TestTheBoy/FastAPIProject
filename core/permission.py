from enum import Enum
from typing import List,Optional,Union
from fastapi import Depends,Request,FastAPI
from fastapi.responses import JSONResponse

from App_Demo.user_context import UserContext


class SaMode(Enum):
    """
    权限检查模式枚举
    """
    AND = "and"
    OR = "or"

#获取当前用户信息的依赖项
#

class SaCheckPermission:
    """
    权限检查装饰器，用于限制访问特定接口

    """
    def  __init__(
        self,
        value: Optional[Union[str, List[str]]] = None,
        type: str = "",
        mode: SaMode = SaMode.AND,
        or_role: Optional[List[str]] = None,
    ):
        """
        初始化权限检查装饰器
        :param value:权限码，可以是字符串或字符串列表
        :param type:权限类型
        :param mode:权限检查模式(AND 或 OR)
        :param or_role:角色列表，满足任意角色即可访问
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

    def __call__(self, func):   # 被装饰的函数
        #通过装饰器保存权限检查信息到函数属性
        func.__sa_check_permission__ = self
        print(f"{func.__name__}权限码：{self.value},模型：{self.mode}")
        print(func.__sa_check_permission__)
        return func


class SaIgnore:
    '''
    忽略权限检查装饰器

    '''
    def __call__(self, func):
        #标记函数为忽略权限检查
        func.__sa_ignore__ = True
        return func
    
class SaTokenException(Exception):
    """令牌相关基础异常"""
    def __init__(self, message: str = "Token无效或已过期", status_code: int = 401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotLoginException(SaTokenException):
    """未登录异常（通常对应 HTTP 401）"""
    def __init__(self, message: str = "未登录，请先登录"):
        super().__init__(message=message, status_code=401)


class NotPermissionException(SaTokenException):
    """无权限异常（通常对应 HTTP 403）"""
    def __init__(self, message: str = "无此操作权限"):
        super().__init__(message=message, status_code=403)

