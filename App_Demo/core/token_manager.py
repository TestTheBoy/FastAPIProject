"""
令牌管理器

提供全局单例的 TokenStore 访问入口，
应用启动时通过 init_store() 注入具体实现。
"""

from typing import Optional

from App_Demo.core.token_store import TokenStore


class TokenManager:
    """令牌管理器 - 持有全局 TokenStore 实例"""

    _store: Optional[TokenStore] = None

    @classmethod
    def init_store(cls, store: TokenStore) -> None:
        """
        初始化令牌存储（应用启动时调用一次）

        :param store: TokenStore 实现实例
        """
        cls._store = store

    @classmethod
    def get_store(cls) -> TokenStore:
        """
        获取当前令牌存储实例

        :return: TokenStore 实例
        :raises RuntimeError: 尚未初始化
        """
        if cls._store is None:
            raise RuntimeError(
                "TokenManager 尚未初始化，请先在应用启动时调用 TokenManager.init_store()"
            )
        return cls._store

    # ------------------------------------------------------------------
    # 便捷代理方法
    # ------------------------------------------------------------------

    @classmethod
    def save(cls, token: str, user_id: str, expire: int = 3600) -> None:
        cls.get_store().save(token, user_id, expire)

    @classmethod
    def get(cls, token: str) -> Optional[str]:
        return cls.get_store().get(token)

    @classmethod
    def remove(cls, token: str) -> None:
        cls.get_store().remove(token)

    @classmethod
    def exists(cls, token: str) -> bool:
        return cls.get_store().exists(token)

    @classmethod
    def remove_by_user_id(cls, user_id: str) -> None:
        cls.get_store().remove_by_user_id(user_id)
