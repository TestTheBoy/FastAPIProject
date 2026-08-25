import redis
import json
from pydantic import BaseModel
from typing import Optional, TypeVar, Collection, Dict, Union, Generic, Type
from core.cache import CacheOperator
from core.constant_context_holder import ConstantContextHolder

T = TypeVar('T')


class AbstractRedisCacheOperator(CacheOperator, Generic[T]):
    """
    基于 Redis 的缓存封装抽象类

    继承自 CacheOperator，提供 Redis 存储的通用实现。
    子类只需指定 key_prefix 即可快速构建具体缓存类。

    使用示例::

        class DictCache(AbstractRedisCacheOperator[DictVO]):
            def __init__(self, redis_client: redis.Redis):
                super().__init__(redis_client, model_class=DictVO, key_prefix="dict:")
    """

    def __init__(self, redis_client: redis.Redis = None, model_class: Type[T] = None, key_prefix: str = ""):
        self.redis_client = redis_client
        self.cache_key_prefix = ConstantContextHolder.get_cache_key_prefix()
        self.model_class = model_class
        self.key_prefix = key_prefix
        # 当 Redis 不可用时，降级使用内存字典缓存
        self._memory_fallback: Dict[str, T] = {}

    # ------------------------------------------------------------------
    # 内部工具方法
    # ------------------------------------------------------------------

    def _build_key(self, key: str) -> str:
        """构建完整的 Redis 键名：系统前缀 + 业务前缀 + key"""
        return f"{self.cache_key_prefix}{self.key_prefix}{key}"

    def _serialize_value(self, value: T) -> str:
        """
        序列化值为字符串

        支持类型：
        - Pydantic BaseModel：调用 model_dump_json()
        - str：直接返回
        - 其他类型：json.dumps(default=str) 兜底

        :param value: 待序列化的值
        :return: 序列化后的 JSON 字符串
        """
        if value is None:
            return ""
        if isinstance(value, BaseModel):
            return value.model_dump_json()
        if isinstance(value, str):
            return value
        return json.dumps(value, ensure_ascii=False, default=str)

    def _deserialize_value(self, value: bytes) -> T:
        """
        反序列化 Redis 返回的字节数据为对象

        - 若注册了 model_class（Pydantic 模型），则调用 model_validate_json 还原
        - 否则返回解码后的字符串

        :param value: Redis 返回的 bytes
        :return: 反序列化后的对象
        """
        if value is None:
            return None
        text = value.decode('utf-8') if isinstance(value, bytes) else str(value)
        if self.model_class is not None and issubclass(self.model_class, BaseModel):
            return self.model_class.model_validate_json(text)
        return text

    # ------------------------------------------------------------------
    # CacheOperator 接口实现
    # ------------------------------------------------------------------

    def get(self, key: str) -> Optional[T]:
        """
        获取缓存值，Redis 不可用时回退到内存字典

        :param key: 缓存键
        :return: 缓存值
        """
        if self.redis_client:
            full_key = self._build_key(key)
            val = self.redis_client.get(full_key)
            if val is None:
                return None
            return self._deserialize_value(val)
        return self._memory_fallback.get(key)

    def set(self, key: str, value: T, expire: int = None) -> None:
        """
        设置缓存值

        :param key: 缓存键
        :param value: 缓存值
        :param expire: 过期时间（秒），None 表示不过期
        """
        if self.redis_client:
            full_key = self._build_key(key)
            serialized = self._serialize_value(value)
            if expire:
                self.redis_client.setex(full_key, expire, serialized)
            else:
                self.redis_client.set(full_key, serialized)
        else:
            self._memory_fallback[key] = value

    def remove(self, key: str) -> None:
        """
        删除缓存

        :param key: 缓存键
        """
        if self.redis_client:
            full_key = self._build_key(key)
            self.redis_client.delete(full_key)
        else:
            self._memory_fallback.pop(key, None)

    def exists(self, key: str) -> bool:
        """
        检查键是否存在

        :param key: 缓存键
        :return: 存在返回 True
        """
        if self.redis_client:
            full_key = self._build_key(key)
            return self.redis_client.exists(full_key) > 0
        return key in self._memory_fallback

    def get_all_values(self) -> Collection[T]:
        """
        获取缓存中所有值

        通过模式匹配扫描 Redis 中所有匹配前缀的键，
        反序列化后返回值的集合。

        :return: 所有缓存值的列表
        """
        if self.redis_client:
            pattern = f"{self.cache_key_prefix}{self.key_prefix}*"
            keys = self.redis_client.keys(pattern)
            values = []
            for k in keys:
                val = self.redis_client.get(k)
                if val is not None:
                    values.append(self._deserialize_value(val))
            return values
        return list(self._memory_fallback.values())

    def get_all_key_values(self) -> Dict[str, T]:
        """
        获取缓存中所有键值对

        键名会去掉系统前缀和业务前缀，只保留业务键部分。

        :return: 键值对字典
        """
        if self.redis_client:
            pattern = f"{self.cache_key_prefix}{self.key_prefix}*"
            keys = self.redis_client.keys(pattern)
            prefix_len = len(self.cache_key_prefix) + len(self.key_prefix)
            result: Dict[str, T] = {}
            for k in keys:
                val = self.redis_client.get(k)
                if val is not None:
                    short_key = k.decode('utf-8')[prefix_len:]
                    result[short_key] = self._deserialize_value(val)
            return result
        return dict(self._memory_fallback)
