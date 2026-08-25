import math
from datetime import datetime
from itertools import count
from typing import Union, List, Generic, TypeVar, Optional, Any

from sqlalchemy import BigInteger, Column, DateTime, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Query
from pydantic import BaseModel, Field, field_serializer
from sqlalchemy.orm import Session

from App_Demo.user_context import UserContext
from App_Demo.util import OrmUtil

T = TypeVar('T') # 泛型,增强返回模型的清晰度
Base = declarative_base()

class BaseOrmModel(Base):
    '''
    基础参数,普通模型基类
    '''
    __abstract__ = True #表明这是一个抽象基类
    id = Column("id", BigInteger, primary_key=True, comment="用户ID", nullable=False, default=OrmUtil.generate_id)
    # 时间戳字段
    createTime = Column("create_time", DateTime, comment="创建时间", nullable=True,default=datetime.now)
    createUser = Column("create_user", BigInteger, comment="创建用户", nullable=True,default=UserContext.get_current_user_id,onupdate=UserContext.get_current_user_id)#UserContext.get_current_user_id拿取用户信息
    updateTime = Column("update_time", DateTime, comment="更新时间", nullable=True,default =datetime.now)
    updateUser = Column("update_user", BigInteger, comment="更新用户", nullable=True,default=UserContext.get_current_user_id,onupdate=UserContext.get_current_user_id)
    # 逻辑删除字段
    isDeleted = Column("is_deleted", Integer, comment="是否删除", nullable=True, default=False)

    @classmethod
    def remove_by_ids(cls, ids: List[str], db: Session):
        """
        逻辑删除
        """
        # 通过检查类属性而不是实例属性来判断是否存在逻辑删除字段
        # 如果类中定义了isDeleted且不为None，则使用逻辑删除
        if OrmUtil.has_logic_delete_field(cls):
            # 执行逻辑删除
            db.query(cls).filter(cls.id.in_(ids)).update({'isDeleted': 1})
        else:
            # 物理删除
            models = db.query(cls).filter(cls.id.in_(ids)).all()
            for model in models:
                db.delete(model)

class IdParam(BaseModel):
    id: Union[str,int] = Field(...,description="ID")

class IdsParam(BaseModel):
    ids: List[Union[str,int]] = Field(...,description="IDs")


class BasePageParam(BaseModel):
    pageNum: int = Field(1, description="当前页")
    pageSize: int = Field(10, description="每页大小")
    orderBy: Union[str, None] = Field(None, description="排序字段")
    keywords: Union[str,None] = Field(None, description="搜索关键字")
    searchKeys: Union[str,None] = Field(None, description="搜索字段")
    labelKey: Union[str, None] = Field("name", description="标签字段")
    valueKey: Union[str, None] = Field("id", description="值字段")
    extFieldNames: Union[str, None] = Field(None, description="扩展字段名称")
    includeType: Union[int, None] = Field(None, description="包含类型(1:增量；2：仅包含)")
    includeIds: Union[List[str], None] = Field(None, description="包含的ID")

class CommonResult(BaseModel,Generic[T]):
    '''
    通用返回结果
    '''
    code: int = Field(0,description="状态码(0:成功,其他失败)")
    msg: str = Field("成功",description="消息描述")
    data: Optional[T] = Field(None,description="返回的数据")
    
class CommonPage(BaseModel,Generic[T]):
    '''
    通用分页数据实体返回结果
    '''
    recordCount: int = Field(0,description="记录总数")
    totalPage: int = Field(0,description="总页数")
    pageSize: int = Field(10,description="每页大小")
    pageNum: int = Field(1,description="当前页")
    rows: List[T] = Field([],description="数据列表")
    #扩展数据（便于添加除了分页相关之外的数据，如有些tab的待处理数、已完成数等）
    ext: Optional[dict] = Field(None,description="扩展数据")

    @classmethod
    def to_page(cls,query:Query, page_num,page_size,vo_class=None,row_handler=None,ext=None):
        '''
        将查询结果转换为分页的数据
        :param query:SQLAlchemy 查询对象
        :param page_num:页码，从1开始
        :param page_size:每页大小
        :param vo_class:VO（Value Object）类，用于数据转换
        :param row_handler:行处理函数
        :param ext:扩展数据
        :return:CommonPage对象
        '''
        if page_num is None or page_num < 1:
            page_num = 1
        recordCount = query.count()
        query = query.offset(page_num-1)
        if not (page_size is None or page_size < 1):
            query = query.limit(page_size)
        records = query.all()
        rows = []
        for record in records:
            vo = OrmUtil.to_vo(ormObj=record,vo_class=vo_class,row_handler=row_handler)
            rows.append(vo)
        totalPage = math.ceil(recordCount/page_size)
        return cls(recordCount=recordCount,totalPage=totalPage,pageSize=page_size,pageNum=page_num,rows=rows,ext=ext)

class APIModel(BaseModel):
    '''
    API模型
    '''
    id: Optional[str] = Field(None,description="ID")
    createTime: Optional[datetime] = Field(None,description="创建时间")
    updateTime: Optional[datetime] = Field(None,description="更新时间")
    createUser: Optional[Union[int, str]] = Field(None,description="创建用户")
    updateUser: Optional[Union[int, str]] = Field(None,description="更新用户")
    isDeleted: Optional[bool] = Field(False,description="是否删除")

    @field_serializer("createTime")  # 序列化时间字段
    def serializer_createTime(self,v:datetime) -> str:
        if v is None:
            return None
        return v.strftime("%Y-%m-%d %H:%M:%S")

    @field_serializer("updateTime")
    def serializer_updateTime(self,v:datetime) -> str:
        if v is None:
            return None
        return v.strftime("%Y-%m-%d %H:%M:%S")

    @field_serializer("id")
    def serializer_id(self, v: Union[str, int]) -> str:
        if v is None:
            return None
        return str(v)


class R:
    @staticmethod
    def success(msg="成功") -> CommonResult:
        """
        返回成功结果
        :param msg: 消息描述
        :return: CommonResult
        """
        return CommonResult(code=0, msg=msg)

    @staticmethod
    def fail(msg: str, code: int = 99999999) -> CommonResult:
        """
        返回失败结果
        :param msg: 消息描述
        :param code: 状态码
        :return: CommonResult
        """
        return CommonResult(code=code, msg=msg)

    @staticmethod
    def data(data: Any) -> CommonResult:
        """
        返回带有数据的成功结果
        :param data: 返回的数据
        :return: CommonResult
        """
        return CommonResult(data=data)

    @staticmethod
    def data_with_msg(data: Any, msg: str) -> CommonResult:
        """
        返回带有数据的成功结果
        :param data: 返回的数据
        :param msg: 描述
        :return: CommonResult
        """
        return CommonResult(data=data, msg=msg)

    @staticmethod
    def fail_with_code(code: int, msg: str) -> CommonResult:
        """
        根据指定的code和msg返回失败结果
        :param code: 状态码
        :param msg: 消息描述
        :return: CommonResult
        """
        return CommonResult(code=code, msg=msg)