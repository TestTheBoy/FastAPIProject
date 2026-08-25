from typing import List
from App_Demo.base import CommonPage
from App_Demo.low_code_util import LowCodeUtil
from App_Demo.util import OrmUtil
from modules.sys.models.post import PostOrmModel
from modules.sys.params.post_param import PostPageParam, PostParam
from modules.sys.vos.post_vo import PostVO
from sqlalchemy.orm import Session, Query


class PostService:
    def __init__(self, db: Session):
        self.model = PostOrmModel
        self.db = db

    """
    岗位服务
    """
    def save(self, param: PostParam):
        """
        保存岗位
        :param param: 岗位参数
        :return: bool
        """
        LowCodeUtil.check_unique(self.db.query(self.model), "code", param.code, param.id, "岗位编码已存在")
        # 将参数对象转换为字典
        param_dict = param.model_dump(exclude_unset=True)
        # 移除id字段，确保使用系统生成的ID
        param_dict.pop('id', None)
        # 创建模型实例
        model = self.model(**param_dict)
        self.db.add(model)
        self.db.flush()
        return True

    def update(self, param: PostParam):
        """
        修改岗位（部分更新）
        :param param: 岗位参数
        :return: bool
        """
        LowCodeUtil.check_unique(self.db.query(self.model), "code", param.code, param.id, "岗位编码已存在")
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
        删除岗位（逻辑删除）
        :param ids: 岗位id集合
        :return: bool
        """
        self.model.remove_by_ids(ids, self.db)
        self.db.flush()
        return True

    def detail(self, id: str) -> PostVO:
        """
        岗位详情
        :param id: 岗位id
        :return: PostVO
        """
        model = self.db.query(self.model).get(id)
        if not model:
            return None
        # 使用OrmUtil工具将model转换成vo
        return OrmUtil.to_vo(model, PostVO)

    def list(self, param: PostPageParam) -> List[PostVO]:
        """
        查询岗位列表
        :param param: 查询参数
        :return: 岗位列表
        """
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转换为vo-list
        return OrmUtil.to_list(query, PostVO)

    def page(self, param: PostPageParam) -> CommonPage[PostVO]:
        """
        分页查询岗位
        :param param: 查询参数
        :return: 岗位列表
        """
        pageNum = param.pageNum
        pageSize = param.pageSize
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转成通用分页对象
        return CommonPage.to_page(query, page_num=pageNum, page_size=pageSize, vo_class=PostVO)