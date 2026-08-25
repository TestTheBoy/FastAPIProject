"""
Redis 令牌存储实现
"""

import redis
from typing import Optional

from App_Demo.core.constant_context_holder import ConstantContextHolder
from App_Demo.core.token_store import TokenStore


class RedisTokenStore(TokenStore):
    """
    基于 Redis 的令牌存储

    使用 Redis 的 String / Set 结构存储令牌映射：
        token:{token}          → user_id（String，带过期）
        user_tokens:{user_id}  → Set of tokens（用于按用户批量操作）
    """

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.prefix = ConstantContextHolder.get_cache_key_prefix() + "token:"
        self.user_token_prefix = ConstantContextHolder.get_cache_key_prefix() + "user_tokens:"

    # ------------------------------------------------------------------
    # TokenStore 接口实现
    # ------------------------------------------------------------------

    def save(self, token: str, user_id: str, expire: int = 3600) -> None:
        key = f"{self.prefix}{token}"
        self.redis.setex(key, expire, user_id)
        # 维护用户 → 令牌集合，便于按用户批量操作
        user_key = f"{self.user_token_prefix}{user_id}"
        self.redis.sadd(user_key, token)
        self.redis.expire(user_key, expire)

    def get(self, token: str) -> Optional[str]:
        key = f"{self.prefix}{token}"
        val = self.redis.get(key)
        return val.decode('utf-8') if val else None

    def remove(self, token: str) -> None:
        key = f"{self.prefix}{token}"
        user_id = self.redis.get(key)
        if user_id:
            user_id = user_id.decode('utf-8')
            user_key = f"{self.user_token_prefix}{user_id}"
            self.redis.srem(user_key, token)
        self.redis.delete(key)

    def exists(self, token: str) -> bool:
        key = f"{self.prefix}{token}"
        return self.redis.exists(key) > 0

    def remove_by_user_id(self, user_id: str) -> None:
        """移除指定用户的所有令牌（强制注销）"""
        user_key = f"{self.user_token_prefix}{user_id}"
        tokens = self.redis.smembers(user_key)
        for token in tokens:
            token_str = token.decode('utf-8') if isinstance(token, bytes) else token
            self.redis.delete(f"{self.prefix}{token_str}")
        self.redis.delete(user_key)
