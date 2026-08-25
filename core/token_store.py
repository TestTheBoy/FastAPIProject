"""
令牌存储抽象接口

定义令牌持久化操作规范，支持不同后端实现（Redis / 内存等）。
"""

from abc import ABC, abstractmethod
from typing import Optional


class TokenStore(ABC):
    """令牌存储抽象基类"""

    @abstractmethod
    def save(self, token: str, user_id: str, expire: int = 3600) -> None:
        """
        保存令牌

        :param token: JWT 令牌字符串
        :param user_id: 用户 ID
        :param expire: 过期时间（秒）
        """
        ...

    @abstractmethod
    def get(self, token: str) -> Optional[str]:
        """
        获取令牌对应的用户 ID

        :param token: JWT 令牌字符串
        :return: 用户 ID，不存在则返回 None
        """
        ...

    @abstractmethod
    def remove(self, token: str) -> None:
        """
        移除令牌（登出/踢下线）

        :param token: JWT 令牌字符串
        """
        ...

    @abstractmethod
    def exists(self, token: str) -> bool:
        """
        检查令牌是否存在

        :param token: JWT 令牌字符串
        :return: 存在返回 True
        """
        ...

    @abstractmethod
    def remove_by_user_id(self, user_id: str) -> None:
        """
        移除指定用户的所有令牌（强制注销）

        :param user_id: 用户 ID
        """
        ...
