from typing import List
from App_Demo.base import CommonPage
from App_Demo.low_code_util import LowCodeUtil
from App_Demo.util import OrmUtil
from modules.sys.models.dict import DictOrmModel
from modules.sys.models.dict_item import DictItemOrmModel
from modules.sys.params.dict_param import DictPageParam, DictParam
from modules.sys.vos.dict_item_vo import DictItemVO
from modules.sys.vos.dict_vo import DictVO, LabelValueVO
from sqlalchemy.orm import Session, Query


class DictService:
    def __init__(self, db: Session):
        self.model = DictOrmModel
        self.db = db

    """
    字典服务
    """
    def save(self, param: DictParam):
        """
        保存字典
        :param param: 字典参数
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

    def update(self, param: DictParam):
        """
        修改字典（部分更新）
        :param param: 字典参数
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
        删除字典（逻辑删除）
        :param ids: 字典id集合
        :return: bool
        """
        self.model.remove_by_ids(ids, self.db)
        self.db.flush()
        return True

    def detail(self, id: str) -> DictVO:
        """
        字典详情
        :param id: 字典id
        :return: DictVO
        """
        model = self.db.query(self.model).get(id)
        if not model:
            return None
        # 使用OrmUtil工具将model转换成vo
        return OrmUtil.to_vo(model, DictVO)

    def list(self, param: DictPageParam) -> List[DictVO]:
        """
        查询字典列表
        :param param: 查询参数
        :return: 字典列表
        """
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转换为vo-list
        return OrmUtil.to_list(query, DictVO)

    def page(self, param: DictPageParam) -> CommonPage[DictVO]:
        """
        分页查询字典
        :param param: 查询参数
        :return: 字典列表
        """
        pageNum = param.pageNum
        pageSize = param.pageSize
        # 构建动态查询条件
        query: Query = self.db.query(self.model)
        if param.m_IN_groupCode:
            query = query.filter(self.model.groupCode.in_(param.m_IN_groupCode))
        if param.m_LIKE_name:
            query = query.filter(self.model.name.like(f"%{param.m_LIKE_name}%"))
        
        # 转成通用分页对象
        return CommonPage.to_page(query, page_num=pageNum, page_size=pageSize, vo_class=DictVO)

    def get_by_dict_type(self, dict_type: str) -> List[LabelValueVO]:
        '''
        根据字典类型查询字典
        :param dict_type: 字典类型
        :return: 字典列表

        '''
        dictModel: DictOrmModel = self.db.query(self.model).filter(self.model.code == dict_type).first()
        if not dictModel:
            return []
        query : Query = self.db.query(DictItemOrmModel).filter(DictItemOrmModel.dictId == dictModel.id)
        dictItemList:List[DictItemVO] = OrmUtil.to_list(query, DictItemVO)
        res:List[LabelValueVO] = []
        for dictItem in dictItemList:
            if dictModel.dataType == 2:
                #int类型
                res.append(LabelValueVO(label=dictItem.name, value=int(dictItem.code)))
            else:
                res.append(LabelValueVO(label=dictItem.name, value=dictItem.code))

        return res
