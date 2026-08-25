from sqlalchemy import Column, BigInteger, DateTime, Boolean, String, Integer, Text, SmallInteger, Numeric
from sqlalchemy import ForeignKey, UniqueConstraint, Index, func
from datetime import datetime


class DBTypes:
    """
    统一管理常用的SQLAlchemy数据库类型，方便代码生成器使用
    """
    # 基础类型
    Column = Column
    BigInteger = BigInteger
    DateTime = DateTime
    Boolean = Boolean
    String = String
    Integer = Integer
    Text = Text
    SmallInteger = SmallInteger
    Numeric = Numeric
    # 常用约束和关系
    ForeignKey = ForeignKey
    UniqueConstraint = UniqueConstraint
    Index = Index
    # 常用函数
    func = func
    # 常用默认值
    DEFAULT_CREATE_TIME = datetime.now
    DEFAULT_UPDATE_TIME = datetime.now


# 创建全局实例，方便使用obj.xx方式访问
db_types = DBTypes()
