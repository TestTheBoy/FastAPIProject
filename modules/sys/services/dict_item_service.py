from typing import List
from App_Demo.base import CommonPage
from App_Demo.low_code_util import LowCodeUtil
from App_Demo.util import OrmUtil
from modules.sys.models.dict_item import DictItemOrmModel
from modules.sys.params.dict_item_param import DictItemPageParam, DictItemParam
from modules.sys.vos.dict_item_vo import DictItemVO
from sqlalchemy.orm import Session, Query


class DictItemService:
    def __init__(self, db: Session):
        self.model = DictItemOrmModel
        self.db = db

    """
    字典项服务
    """
    def save(self, param: DictItemParam):
        """
        保存字典项
        :param param: 字典项参数
        :return: bool
        """
        # 将参数对象转换为字典
        param_dict = param.model_dump(exclude_unset=True)
        # 移除id字段，确保使用系统生成的ID
        param_dict.pop('id', None)
        # 创建模型实例
        model = self.model(**param_dict)
        self.db.add(model)
        self.db.flush()
        return True

    def update(self, param: DictItemParam):
        """
        修改字典项（部分更新）
        :param param: 字典项参数
        :return: bool
        """
        # 将参数对象转换为字典，只包含设置过的字段
        param_dict = param.model_dump(exclude_unset=True)
        # 移除id字段，避免更新id
        param_dict.pop('id', None)
        # 直接更新数据库记录
        self.db.query(self.model).filter(self.model.id == param.id).update(param_dict)
        self.db.flush()
        return True

    def remove_by_ids(self, ids: List[str]):
        """
        删除字典项（逻辑删除）
        :param ids: 字典项id集合
        :return: bool
        """
        self.model.remove_by_ids(ids, self.db)
        self.db.flush()
        return True

    def detail(self, id: str) -> DictItemVO:
        """
        字典项详情
        :param id: 字典项id
        :return: DictItemVO
        """
        model = self.db.query(self.model).get(id)
        if not model:
            return None
        # 使用OrmUtil工具将model转换成vo
        return OrmUtil.to_vo(model, DictItemVO)

    def list(self, param: DictItemPageParam) -> List[DictItemVO]:
        """
        查询字典项列表
        :param param: 查询参数
        :return: 字典项列表
        """
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转换为vo-list
        return OrmUtil.to_list(query, DictItemVO)

    def page(self, param: DictItemPageParam) -> CommonPage[DictItemVO]:
        """
        分页查询字典项
        :param param: 查询参数
        :return: 字典项列表
        """
        pageNum = param.pageNum
        pageSize = param.pageSize
        # 构建动态查询条件
        query: Query = self.db.query(self.model)
        if param.M_EQ_dictId:
            query = query.filter(self.model.dictId == param.M_EQ_dictId)
        if param.m_LIKE_name:
            query = query.filter(self.model.name.like(f"%{param.m_LIKE_name}%"))
        if param.m_LIKE_code:
            query = query.filter(self.model.code.like(f"%{param.m_LIKE_code}%"))
        #转成通用分页对象
        return CommonPage.to_page(query, page_num=pageNum, page_size=pageSize, vo_class=DictItemVO)