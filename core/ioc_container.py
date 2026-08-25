import importlib
from typing import Any, Dict, Optional

# 模块级状态，替代原来的类变量
_services: Dict[str, Any] = {}
_service_configs: Dict[str, Dict[str, Any]] = {}


def register(service_name: str, module_path_or_instance, class_name: str = None, singleton: bool = True) -> None:
    """
    注册服务（支持两种方式）

    方式一：注册实例
        register("MyService", my_service_instance)

    方式二：延迟加载（模块路径 + 类名）
        register("MyService", "modules.xxx.service", "MyServiceClass")

    :param service_name: 服务名称
    :param module_path_or_instance: 模块路径（字符串）或服务实例
    :param class_name: 类名（方式二必传）
    :param singleton: 是否单例，默认 True
    """
    if isinstance(module_path_or_instance, str):
        # 方式二：延迟加载
        _service_configs[service_name] = {
            "module_path": module_path_or_instance,
            "class_name": class_name,
            "singleton": singleton
        }
        if service_name in _services and not singleton:
            del _services[service_name]
    else:
        # 方式一：直接注册实例
        _services[service_name] = module_path_or_instance


def get_service(service_name: str, *args, **kwargs) -> Any:
    """
    获取服务实例

    :param service_name: 注册的服务名称
    :param args: 传递给构造函数的位置参数
    :param kwargs: 传递给构造函数的关键字参数
    :return: 服务实例
    :raises ValueError: 服务未注册
    :raises ImportError: 导入模块或类失败
    :raises Exception: 实例化失败
    """
    # 1. 检查是否已有缓存实例（单例）
    if service_name in _services:
        return _services[service_name]

    # 2. 获取服务配置
    config = _service_configs.get(service_name)
    if not config:
        raise ValueError(f"Service '{service_name}' is not registered.")

    module_path = config["module_path"]
    class_name = config["class_name"]
    is_singleton = config["singleton"]

    # 3. 动态导入模块和类
    try:
        module = importlib.import_module(module_path)
        service_class = getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(f"Failed to load service '{service_name}': {e}")

    # 4. 实例化
    try:
        instance = service_class(*args, **kwargs)
    except Exception as e:
        raise Exception(f"Failed to instantiate service '{service_name}': {e}")

    # 5. 单例则缓存
    if is_singleton:
        _services[service_name] = instance

    return instance


def clear() -> None:
    """清除所有缓存的服务实例（主要用于测试）"""
    _services.clear()


# 可选：预注册示例（取消注释并按需使用）
# register("low_code_service", "modules.sys.services.low_code_service", "LowCodeService")