"""
常量上下文 - 系统配置的内存缓存

与 ConstantContextHolder（环境变量读取）不同，
ConstantContext 用于存储从数据库加载的运行时配置常量，
在应用启动时由 ConfigService.init_config_cache() 初始化。
"""

from typing import Any, Dict, Optional


class ConstantContext:
    """
    系统配置常量上下文

    以类级别字典存储运行时配置，提供 get / set / clear 操作。
    配置数据在应用启动时从数据库 config 表加载，
    通过 ConstantContextHolder 可读取环境变量级别的配置。

    使用示例::

        # 启动时加载
        ConstantContext.set("sys_name", "管理系统")
        ConstantContext.set("upload_max_size", "100")

        # 运行时读取
        name = ConstantContext.get("sys_name")
    """

    _context: Dict[str, Any] = {}

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        设置配置项

        :param key: 配置键
        :param value: 配置值
        """
        cls._context[key] = value

    @classmethod
    def get(cls, key: str, default: Any = None) -> Optional[Any]:
        """
        获取配置项

        :param key: 配置键
        :param default: 不存在时返回的默认值
        :return: 配置值
        """
        return cls._context.get(key, default)

    @classmethod
    def remove(cls, key: str) -> None:
        """
        移除配置项

        :param key: 配置键
        """
        cls._context.pop(key, None)

    @classmethod
    def clear(cls) -> None:
        """清空所有配置项"""
        cls._context.clear()

    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """
        获取所有配置项（返回副本，防止外部修改）

        :return: 配置字典副本
        """
        return dict(cls._context)

    @classmethod
    def size(cls) -> int:
        """
        获取配置项数量

        :return: 配置项数量
        """
        return len(cls._context)
