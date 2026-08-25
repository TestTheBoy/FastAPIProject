#业务层/
from idlelib.query import Query
from typing import List, Optional

from fastapi import Request
from sqlalchemy.orm import Session, aliased

from App_Demo.base import CommonPage, BasePageParam
from App_Demo.low_code_util import LowCodeUtil
from App_Demo.user_context import UserContext
from App_Demo.util import OrmUtil, StrUtil
from core.exception import AssertTool
from modules.sys.models.dept import DeptOrmModel
from modules.sys.models.post import PostOrmModel
from modules.sys.models.user import UserOrmModel
from modules.sys.models.user_role import UserRoleOrmModel
from modules.sys.params.user_param import UpdateUserAvatarParam, UpdateUserInfoParam, UpdateUserpwdParam, UserParam, UserPageParam
from modules.sys.vos.auth_vo import LoginUser
from modules.sys.vos.dict_vo import LabelValueVO
from modules.sys.vos.user_role_vo import UserRoleVO
from modules.sys.vos.user_vo import UserVO

try:
    from config import IMG_BASE_URL
except Exception:
    IMG_BASE_URL = "http://localhost:8000/uploadfiles/"

DEFAULT_PASSWORD = "123456"


def _build_avatar_url(avatar: Optional[str], request: Optional[Request] = None) -> Optional[str]:
    if not avatar or avatar.startswith(("http://", "https://")):
        return avatar
    avatar = f"/uploadfiles/{avatar.lstrip('/')}" if not avatar.startswith("/uploadfiles/") else avatar
    return f"{str(request.base_url).rstrip('/')}{avatar}" if request else avatar


class UserService:
    '''
    用户服务类
    '''
    def __init__(self,db: Session):
        self.model = UserOrmModel
        self.db = db

    def save(self,param: UserParam) -> bool:
        '''
        保存用户
        :param param:用户参数
        :return: bool
        '''
        self._check_unique(param)
        #将参数对象转换为字典
        salt = StrUtil.random_string(8)
        encryptPassword = StrUtil.md5_encrypt(str(param.password)+salt)
        if not param.isLocked:
            param.isLocked = 0
        if not param.password:
            param.password = DEFAULT_PASSWORD
        # 只能添加普通管理员账号
        param.adminType = 2
        param_dict = param.model_dump(exclude_unset= True) #获取参数字典,表示只包含在原始数据中明确设置的字段，排除未设置或使用默认值的字段
        param_dict['salt'] = salt
        param_dict['password'] = encryptPassword
        #移除id字段，确保使用系统生成的ID
        param_dict.pop('id', None)
        #创建模型实例
        model = self.model(**param_dict)
        self.db.add(model) #添加入库
        self.db.flush()
        return True

    def update(self,param: UserParam) -> bool:
        '''
        更新用户
        :param param:用户参数
        :return: 保存结果
        '''
        self._check_unique(param)
        # 将参数对象转换为字典，只包含设置过的字段
        param_dict = param.model_dump(exclude_unset= True)
        #移除id字段，避免更新id
        param_dict.pop('id', None)
        param_dict.pop('adminType', None)
        param_dict.pop('password', None)  # 避免更新密码
        param_dict.pop('salt', None)  # 避免更新盐值
        #直接更新数据库记录
        self.db.query(self.model).filter(self.model.id == param.id).update(param_dict)
        self.db.flush()
        return True

    def removeByIds(self,ids: List[str]) -> bool:
        '''
        删除用户
        :param param:ids集合
        :return: 保存结果
        '''
        self.model.remove_by_ids(ids, self.db)
        self.db.flush()
        return True

    def detail(self,id: str) -> UserVO:
        '''
        获取用户详情
        :param id:用户id
        :return: 用户详情
        '''

        t_alias = aliased(self.model, name="t")
        d_alias= aliased(DeptOrmModel, name="d")
        p_alias = aliased(PostOrmModel, name="p")
        query: Query = (
            self.db.query(
                t_alias,
                d_alias.name.label("deptName"), #.label强行改名
                d_alias.code.label("deptCode"),
                p_alias.name.label("postName"),
                p_alias.code.label("postCode"),
            )
            .outerjoin(d_alias, t_alias.deptId == d_alias.id)
            .outerjoin(p_alias, t_alias.postId == p_alias.id)
        )
        query = query.filter(t_alias.id == id)
        ormModel = query.one_or_none()
        if not ormModel: return None
        return OrmUtil.to_vo(ormModel, UserVO)
    
    def list(self, param: UserPageParam) -> List[UserVO]:
        """
        查询用户列表
        :param param: 查询参数
        :return: 用户列表
        """
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=self.model,db=self.db, query=None)
        # 转换为vo-list
        return OrmUtil.to_list(query, UserVO)    
    def page(self, param: UserPageParam) -> CommonPage[UserVO]:
        """
        分页查询用户
        :param param: 查询参数
        :return: 用户列表
        """
        pageNum = param.pageNum
        pageSize = param.pageSize
        t_alias = aliased(self.model, name="t")
        d_alias= aliased(DeptOrmModel, name="d")
        p_alias = aliased(PostOrmModel, name="p")
        query: Query = (
            self.db.query(
                t_alias,
                d_alias.name.label("deptName"),
                d_alias.code.label("deptCode"),
                p_alias.name.label("postName"),
                p_alias.code.label("postCode"),
            )
            .outerjoin(d_alias, t_alias.deptId == d_alias.id)
            .outerjoin(p_alias, t_alias.postId == p_alias.id)
            .order_by(d_alias.sort.asc(), p_alias.sort.asc(),t_alias.id.asc())
        )
        # 构建动态查询条件
        
        if param.inUserIdList:
            query = query.filter(t_alias.id.in_(param.inUserIdList))
        if param.notInUserIdList:
            query = query.filter(t_alias.id.notin_(param.notInUserIdList))
        # 超级管理员不允许参与业务，所以排除掉
        query = query.filter(t_alias.adminType != 1)
        # 实现模糊查询
        # if param.keywords:
        #     query = query.filter(
        #         t_alias.userName.like(f'%{param.keywords}%') |
        #         t_alias.realName.like(f'%{param.keywords}%') |
        #         t_alias.nickName.like(f'%{param.keywords}%') |
        #         t_alias.mobilePhone.like(f'%{param.keywords}%') |
        #         t_alias.tel.like(f'%{param.keywords}%')
        #     )
        # 构建动态查询条件
        query: Query = LowCodeUtil.build_query(page_param=param, model=t_alias,db=self.db, query=query)
        #  排除已删除的
        #query = query.filter(t_alias.isDeleted  == 0)
        # 转成通用分页对象
        return CommonPage.to_page(query, page_num=pageNum, page_size=pageSize, vo_class=UserVO, row_handler=self._row_handler)

    def reset_password(self, ids: List[str]) -> bool:
        """
        重置密码
        :param ids:用户id集合
        :return: 重置结果
        """    
        for id in ids:
            salt = StrUtil.random_string(8)
            password = StrUtil.md5_encrypt(DEFAULT_PASSWORD+salt)
            
            self.db.query(UserOrmModel).filter(UserOrmModel.id == id).update({"password": password, "salt": salt})
            self.db.flush()

    def grant_role(self, userId: str, roleIdList: List[str]) :
        """
        授权用户角色
        :param userId:用户id
        :param roleIdList:角色id列表
        :return: bool
        """
        # 先删除用户用户角色关联
        self.db.query(UserRoleOrmModel).filter(UserRoleOrmModel.userId == userId).delete()
        for roleId in roleIdList:
            self.db.add(UserRoleOrmModel(userId=userId, roleId=roleId))
        
        return True
    
    def lock(self, ids: List[str]) -> bool:
        """
        锁定用户
        :param ids:用户id集合
        :return: 锁定结果
        """
        if ids:
            self.db.query(self.model).filter(self.model.id.in_(ids)).update({"isLock": 1})
            self.db.flush()
        return True

    def unlock(self, ids: List[str]) -> bool:
        """
        取消锁定用户
        :param ids:用户id集合
        :return: 锁定结果
        """
        if ids:
            self.db.query(self.model).filter(self.model.id.in_(ids)).update({"isLock": 0})
            self.db.flush()
        return True

    def select(self, param: UserPageParam) -> List[LabelValueVO]:

        param.label =  "realName"
        query: Query = self.db.query(self.model)
        #超级管理员不允许参与业务，所以排除掉
        query = query.filter(self.model.adminType != 1)
        #ERROR:root:maximum recursion depth exceeded while calling a Python object(调用 Python 对象时超出最大递归深度) 
        voList:List[UserVO] = OrmUtil.to_list(query,UserVO)
        return LowCodeUtil.vos_to_lvs(voList=voList,param=param)
    
    def info(self, request: Optional[Request] = None) -> LoginUser:
        loginUser: LoginUser = UserContext.get_current_user()
        userVO: UserVO = self.detail(loginUser.userId)
        if userVO.avatar and not userVO.avatar.startswith(("http://", "https://")):
            userVO.avatar = f"{IMG_BASE_URL}{userVO.avatar}"
        #以数据库的数据为准，覆盖登录用户信息
        userDict = userVO.model_dump() if userVO else {}
        userDict.pop("roleIds")
        return LoginUser(**{**loginUser.model_dump(), **userDict})

    #
    def update_info(self, param: UpdateUserInfoParam) -> bool:
        #设置当前用户id
        # param.id = UserContext.get_current_user().userId
        param_dict = param.model_dump()
        param_dict.pop("id")
        self.db.query(self.model).filter(self.model.id == param.id).update(param_dict)
        self.db.flush()
        return True
    
    #更新用户头像
    def update_avatar(self, param: UpdateUserAvatarParam) -> bool:
        #设置当前用户id
        # param.id = UserContext.get_current_user().userId
        param_dict = param.model_dump()
        param_dict.pop("id")
        self.db.query(self.model).filter(self.model.id == param.id).update(param_dict)
        self.db.flush()
        return True
    
    def update_pwd(self, param: UpdateUserpwdParam) -> bool:
        '''
        更新用户密码
        :param param: 更新参数
        :return: 更新结果
        '''
        if param.newPassword != param.confirmPassword:
            AssertTool.raise_biz_with_msg(code=0,msg="新密码和确认密码不一致")
        
        #校验旧密码是否匹配==> 和数据库密码一致
        userModel: UserOrmModel = self.db.query(UserOrmModel).filter(UserOrmModel.id == param.id).first()
        if not userModel:
            AssertTool.raise_biz_with_msg("用户不存在")
        encryptPassword = StrUtil.md5_encrypt(str(param.password)+userModel.salt)
        if userModel.password != encryptPassword:
            AssertTool.raise_biz_with_msg("旧密码不正确")

        salt = StrUtil.random_string(8)
        password = StrUtil.md5_encrypt(param.newPassword+salt)
        self.db.query(UserOrmModel).filter(UserOrmModel.id == param.id).update({"password": password, "salt": salt})
        self.db.flush()
        return True


    def _check_unique (self,param:UserParam) -> bool:
        """
         检查唯一
         """
        field_list = ["userName","mobilePhone"]
        return all(self._check_unique_by_field(fieldName,param) for fieldName in field_list)

    def _check_unique_by_field(self,fieldName: str,param:UserParam) -> bool:
        """
         检查某个字段唯一
         """
        return LowCodeUtil.check_unique (model_query=self.db.query(self.model),column=fieldName,value=getattr(param,fieldName),id_value=param.id,error_msg=f"{fieldName}已存在")
    
    def _row_handler(self,vo:UserVO):
        """
        处理每一行数据（解决了用户管理角色授权的回显bug）
        """
        userRoleList:List[UserRoleVO]=OrmUtil.to_list(self.db.query(UserRoleOrmModel).filter(UserRoleOrmModel.userId == vo.id),vo_class=UserRoleVO)
        ids = [userRole.roleId for userRole in userRoleList]
        if ids:
            vo.roleIds = ",".join(ids)
        return vo