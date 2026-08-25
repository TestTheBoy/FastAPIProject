# 访问类型枚举
from enum import Enum


class VisTypeEnum(str, Enum):
    """访问日志类型枚举"""
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    PLAY_USER = "PLAY_USER"
    UN_PLAY_USER = "UN_PLAY_USER"
    OTHER = "OTHER"
