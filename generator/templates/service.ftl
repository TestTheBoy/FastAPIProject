from typing import List
from App_Demo.base import CommonPage
from App_Demo.low_code_util import LowCodeUtil
from App_Demo.util import OrmUtil{% if table.treeTable %}, TreeUtil{% endif %}
from modules.{{ table.moduleName }}.models.{{ table.shortTableName }} import {{ table.tableHumpName }}OrmModel
from modules.{{ table.moduleName }}.params.{{ table.shortTableName }}_param import {{ table.tableHumpName }}PageParam, {{ table.tableHumpName }}Param
from modules.{{ table.moduleName }}.vos.{{ table.shortTableName }}_vo import {{ table.tableHumpName }}VO
from sqlalchemy.orm import Session, Query


class {{ table.tableHumpName }}Service:
    def __init__(self, db: Session):
        self.model = {{ table.tableHumpName }}OrmModel
        self.db = db

    """
    {{ table.comment }}服务
    """
    def save(self, param: {{ table.tableHumpName }}Param):
        """
        保存{{ table.comment }}
        :param param: {{ table.comment }}参数
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

    def update(self, param: {{ table.tableHumpName }}Param):
        """
        修改{{ table.comment }}（部分更新）
        :param param: {{ table.comment }}参数
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
        删除{{ table.comment }}（逻辑删除）
        :param ids: {{ table.comment }}id集合
        :return: bool
        """
        self.model.remove_by_ids(ids, self.db)
        self.db.flush()
        return True

    def detail(self, id: str) -> {{ table.tableHumpName }}VO:
        """
        {{ table.comment }}详情
        :param id: {{ table.comment }}id
        :return: {{ table.tableHumpName }}VO
        """
        model = self.db.query(self.model).get(id)
        if not model:
            return None
        # 使用OrmUtil工具将model转换成vo
        return OrmUtil.to_vo(model, {{ table.tableHumpName }}VO)

    def list(self, param: {{ table.tableHumpName }}PageParam) -> List[{{ table.tableHumpName }}VO]:
        """
        查询{{ table.comment }}列表
        :param param: 查询参数
        :return: {{ table.comment }}列表
        """
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转换为vo-list
        return OrmUtil.to_list(query, {{ table.tableHumpName }}VO)

    def page(self, param: {{ table.tableHumpName }}PageParam) -> CommonPage[{{ table.tableHumpName }}VO]:
        """
        分页查询{{ table.comment }}
        :param param: 查询参数
        :return: {{ table.comment }}列表
        """
        pageNum = param.pageNum
        pageSize = param.pageSize
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转成通用分页对象
        return CommonPage.to_page(query, page_num=pageNum, page_size=pageSize, vo_class={{ table.tableHumpName }}VO){% if table.treeTable %}

    def tree(self, param: {{ table.tableHumpName }}PageParam) -> List[{{ table.tableHumpName }}VO]:
        """
        获取{{ table.comment }}树
        :param param: 查询参数
        :return: {{ table.comment }}树
        """
        listData:List[{{ table.tableHumpName }}VO] = self.list(param)
        # 转换为树结构
        return TreeUtil.build_tree(listData){% endif %}