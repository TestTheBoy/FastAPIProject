"""
缓存操作抽象接口模块

设计层次：
    CacheOperator (抽象接口)
        └── AbstractRedisCacheOperator (Redis实现)
                ├── DictCache (字典缓存)
                ├── CaptchaCache (验证码缓存)
                └── ... (其他具体缓存实现)
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Dict, Collection, Optional

T = TypeVar('T')


class CacheOperator(ABC, Generic[T]):
    """
    缓存操作抽象接口

    定义缓存的基本 CRUD 操作规范，所有缓存实现（内存字典、Redis等）
    均需实现此接口，确保上层调用方不感知底层存储细节。
    """

    @abstractmethod
    def get(self, key: str) -> Optional[T]:
        """
        根据键获取缓存值

        :param key: 缓存键
        :return: 缓存值，不存在时返回 None
        """
        ...

    @abstractmethod
    def set(self, key: str, value: T, expire: int = None) -> None:
        """
        设置缓存值

        :param key: 缓存键
        :param value: 缓存值
        :param expire: 过期时间（秒），None 表示不过期
        """
        ...

    @abstractmethod
    def remove(self, key: str) -> None:
        """
        删除缓存

        :param key: 缓存键
        """
        ...

    @abstractmethod
    def exists(self, key: str) -> bool:
        """
        检查键是否存在

        :param key: 缓存键
        :return: 存在返回 True，否则 False
        """
        ...

    @abstractmethod
    def get_all_values(self) -> Collection[T]:
        """
        获取缓存中所有的值列表

        :return: 所有缓存值的集合
        """
        ...

    @abstractmethod
    def get_all_key_values(self) -> Dict[str, T]:
        """
        获取缓存中所有的键值对

        :return: 键值对字典
        """
        ...
