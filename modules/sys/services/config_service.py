from typing import List
from App_Demo.base import CommonPage
from App_Demo.low_code_util import LowCodeUtil
from App_Demo.util import OrmUtil
from core.constant_context import ConstantContext
from modules.sys.enums.yes_no_enum import YesNoEnum
from modules.sys.models.config import ConfigOrmModel
from modules.sys.params.config_param import ConfigPageParam, ConfigParam
from modules.sys.vos.config_vo import ConfigVO
from sqlalchemy.orm import Session, Query


class ConfigService:
    def __init__(self, db: Session):
        self.model = ConfigOrmModel
        self.db = db

    """
    配置服务
    """
    def save(self, param: ConfigParam):
        """
        保存配置
        :param param: 配置参数
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

    def update(self, param: ConfigParam):
        """
        修改配置（部分更新）
        :param param: 配置参数
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
        删除配置（逻辑删除）
        :param ids: 配置id集合
        :return: bool
        """
        self.model.remove_by_ids(ids, self.db)
        self.db.flush()
        return True

    def detail(self, id: str) -> ConfigVO:
        """
        配置详情
        :param id: 配置id
        :return: ConfigVO
        """
        model = self.db.query(self.model).get(id)
        if not model:
            return None
        # 使用OrmUtil工具将model转换成vo
        return OrmUtil.to_vo(model, ConfigVO)

    def list(self, param: ConfigPageParam) -> List[ConfigVO]:
        """
        查询配置列表
        :param param: 查询参数
        :return: 配置列表
        """
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转换为vo-list
        return OrmUtil.to_list(query, ConfigVO)

    def page(self, param: ConfigPageParam) -> CommonPage[ConfigVO]:
        """
        分页查询配置
        :param param: 查询参数
        :return: 配置列表
        """
        pageNum = param.pageNum
        pageSize = param.pageSize
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转成通用分页对象
        return CommonPage.to_page(query, page_num=pageNum, page_size=pageSize, vo_class=ConfigVO)

    def init_config_cache(self) -> None:
        '''
        初始化配置缓存
        将数据库中的配置数据加载到缓存中
        '''
        configs = self.db.query(self.model).filter(
            self.model.deleted == YesNoEnum.Yes.code
        ).all()

        #清空现有配置
        ConstantContext.clear()

        #将配置加载到ConstantContext中
        for config in configs:
            ConstantContext.set(config.code, config.content)

        print(f"初始化配置缓存完成，共有{len(configs)}条配置数据")