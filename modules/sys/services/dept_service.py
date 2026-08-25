from typing import List
from App_Demo.base import CommonPage
from App_Demo.low_code_util import LowCodeUtil
from App_Demo.util import OrmUtil, TreeUtil
from modules.sys.models.dept import DeptOrmModel
from modules.sys.params.dept_param import DeptPageParam, DeptParam
from modules.sys.vos.dept_vo import DeptVO
from sqlalchemy.orm import Session, Query


class DeptService:
    def __init__(self, db: Session):
        self.model = DeptOrmModel
        self.db = db

    """
    部门服务
    """
    def save(self, param: DeptParam):
        """
        保存部门
        :param param: 部门参数
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

    def update(self, param: DeptParam):
        """
        修改部门（部分更新）
        :param param: 部门参数
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
        删除部门（逻辑删除）
        :param ids: 部门id集合
        :return: bool
        """
        self.model.remove_by_ids(ids, self.db)
        self.db.flush()
        return True

    def detail(self, id: str) -> DeptVO:
        """
        部门详情
        :param id: 部门id
        :return: DeptVO
        """
        model = self.db.query(self.model).get(id)
        if not model:
            return None
        # 使用OrmUtil工具将model转换成vo
        return OrmUtil.to_vo(model, DeptVO)

    def list(self, param: DeptPageParam) -> List[DeptVO]:
        """
        查询部门列表
        :param param: 查询参数
        :return: 部门列表
        """
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转换为vo-list
        return OrmUtil.to_list(query, DeptVO)

    def page(self, param: DeptPageParam) -> CommonPage[DeptVO]:
        """
        分页查询部门
        :param param: 查询参数
        :return: 部门列表
        """
        pageNum = param.pageNum
        pageSize = param.pageSize
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转成通用分页对象
        return CommonPage.to_page(query, page_num=pageNum, page_size=pageSize, vo_class=DeptVO)

    def tree(self, param: DeptPageParam) -> List[DeptVO]:
        """
        获取部门树
        :param param: 查询参数
        :return: 部门树
        """
        listData:List[DeptVO] = self.list(param)
        # 转换为树结构
        return TreeUtil.build_tree(listData)