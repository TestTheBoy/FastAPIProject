# 创建上下文变量
from contextvars import ContextVar
from typing import Optional

from modules.sys.vos.auth_vo import LoginUser

current_user_ctx: ContextVar[Optional[LoginUser]] = ContextVar("current_user", default=None)


class UserContext:
    """
    用户上下文
    """

    @staticmethod
    def set_current_user(user: LoginUser):
        """设置当前用户到上下文"""
        current_user_ctx.set(user)

    @staticmethod
    def get_current_user() -> Optional[LoginUser]:
        """从上下文获取当前用户"""
        return current_user_ctx.get()

    @staticmethod
    def get_current_user_id() -> Optional[str]:
        """从上下文获取当前用户ID"""
        user = UserContext.get_current_user()
        if user is None:
            return None
        return user.userId

    @staticmethod
    def get_current_user_name() -> Optional[str]:
        """从上下文获取当前用户名称"""
        user = UserContext.get_current_user()
        if user is None:
            return None
        return user.userName

    @staticmethod
    def is_super_admin() -> bool:
        """判断当前用户是否是超级管理员"""
        user = UserContext.get_current_user()
        if user is None:
            return False
        return user.superAdmin