#身份验证服务
from datetime import datetime
from typing import Union, Dict,List
import hashlib

from sqlalchemy.orm import Session

from App_Demo.sm2_util import Sm2Util
from App_Demo.user_context import UserContext
from App_Demo.core.constant_context_holder import ConstantContextHolder
from App_Demo.core.exception import AssertTool
from App_Demo.util import StrUtil, JwtUtil, OrmUtil
from App_Demo.core.ioc_container import get_service
from modules.sys.enums.vis_type_enum import VisTypeEnum
from modules.sys.models.dept import DeptOrmModel
from modules.sys.models.menu import MenuOrmModel
from modules.sys.models.post import PostOrmModel
from modules.sys.models.role import RoleOrmModel
from modules.sys.models.role_menu import RoleMenuOrmModel
from modules.sys.models.user import UserOrmModel
from modules.sys.models.user_role import UserRoleOrmModel
from modules.sys.params.auth_param import LoginParam
from modules.sys.services.captcha_service import CaptchaService
from modules.sys.services.vis_log_service import VisLogService
from modules.sys.vos.auth_vo import LoginToken,LoginUser
from modules.sys.vos.role_vo import RoleVO
from modules.sys.vos.user_role_vo import UserRoleVO
from modules.sys.vos.role_menu_vo import RoleMenuVO

class AuthService:
    jwt_secret: str = "xK8vN2mP9qL5wR3tY7uI1oA4sD6fG0hJ2kM8nB5cV9xZ"
    def __init__(self, db: Session):
        self.db = db

    def login(self, param: LoginParam) -> LoginToken:
        """
        登录
        :param param: 登录参数
        :return: 登录结果
        """
        vis_log_service: VisLogService = get_service("VisLogService",db=self.db)

        # 1. 提取用户名和密码（SM2 解密后会覆盖 password）
        userName = param.username
        password = param.password

        # 2. 验证码校验（仅开启时）
        if ConstantContextHolder.get_captcha_open_flag():
            captcha_service: CaptchaService = get_service("CaptchaService",db=self.db)
            success:bool = captcha_service.validate(None,None)
            if not success:
                vis_log_service.save_vis_log(
                    visType=VisTypeEnum.LOGIN,
                    account=param.username or 'unknown',
                    success="N",
                    message="验证码错误",
                )
                AssertTool.raise_biz_with_code_msg(10000004, "验证码错误")

        # 3. SM2 密码解密（仅开启时）
        if ConstantContextHolder.get_sm2_open_flag():
            private_key = ConstantContextHolder.get_sm2_private_key()
            try:
                password = Sm2Util.decrypt(private_key, param.password)
            except Exception as e:
                print(f"SM2 decrypt error: {e}")

        # 4. 查询用户（用户名/手机号）
        userModel: UserOrmModel = self.db.query(UserOrmModel).filter(
            UserOrmModel.userName == userName
        ).first()
        if userModel is None:
            userModel = self.db.query(UserOrmModel).filter(
                UserOrmModel.mobilePhone == userName
            ).first()

        if not userModel:
            vis_log_service.save_vis_log(
                visType=VisTypeEnum.LOGIN,
                account=param.username or 'unknown',
                success="N",
                message="用户不存在",
            )
            AssertTool.raise_biz_with_msg("用户名或密码错误")
        if userModel.isLocked == 1:
            AssertTool.raise_biz_with_msg("用户已被锁定，请联系管理员解封")
        encryptPassword = StrUtil.md5_encrypt(str(password) + userModel.salt)
        if userModel.password != encryptPassword:
            AssertTool.raise_biz_with_msg("用户名或密码错误")
        # 登录成功，生成token
        # 当前permCodes是静态的，实际开发中应该从数据库中查询
        # RBAC权限管理 --- (Role-Based Access Control)基于角色的访问控制
        """"
        select * from sys_user where id = 1686404946814533633;
            -- 根据用户id查询其拥有的角色id
            select role_id from sys_user_role where user_id = 1686404946814533633;
            -- 根据角色id获取其菜单id
            select menu_id from sys_role_menu where role_id in(select role_id from sys_user_role where user_id = 1686404946814533633)

            -- 根据菜单id获取权限码

            select code from sys_menu where id in (
            select menu_id from sys_role_menu where role_id in(select role_id from sys_user_role where user_id = 1686404946814533633)
            )
        """
        # permCodes: List[str] = []
        # if userModel.adminType == 1:
        #     permCodes = ["admin"]
        # else:
        #     # 根据用户id查询其拥有的角色id
        #     userRoleQuery = self.db.query(UserRoleOrmModel).filter(UserRoleOrmModel.userId == userModel.id)
        #     userRoleList: List[UserRoleVO] = OrmUtil.to_list(userRoleQuery, UserRoleVO)
        #     roleIds: List[str] = [userRole.roleId for userRole in userRoleList]
        #     if roleIds:
        #         # 根据角色ids获取其菜单id
        #         roleMenuQuery = self.db.query(RoleMenuOrmModel).filter(RoleMenuOrmModel.roleId.in_(roleIds))
        #         roleMenuList: List[RoleMenuVO] = OrmUtil.to_list(roleMenuQuery, RoleMenuVO)
        #         menuIds: List[str] = [roleMenu.menuId for roleMenu in roleMenuList]
        #         if menuIds:
        #             # 根据菜单ids获取权限码
        #             menuQuery = self.db.query(MenuOrmModel).filter(MenuOrmModel.id.in_(menuIds))
        #             permCodes = [menu.code for menu in menuQuery]
        payload = self.to_login_user(userModel)

        token = JwtUtil.generate_token(payload, AuthService.jwt_secret)
        return LoginToken(token=token, userId=str(userModel.id))
    def logout(self, token: Union[str, None]) -> bool:
        '''
        登出
        :param token:登陸令牌
        :return:登出结果
        '''
        if token is None:
            return True
        # 删除 token
        return True
    
    def play_user(self, userId: str)-> LoginToken:
        """
        扮演用户
        :param userId: 用户id
        :return: 登录结果
        """
        # 拿到userId获取对应用户信息进行登录
        # 追加扩展信息：playerUserId/playerAccount/playerToken/isPlayer
        """
        我们先不考虑存token，因为jwt的话，两个token可能会太长，特别是有权限码的情况下。
        login_user.ext["playerToken"] = RequestContext.get_token()
        login_user.ext["playerUserId"] = current_user.id
        login_user.ext["playerAccount"] = current_user.userName
        login_user.ext["isPlayer"] = True
        """
        userModel: UserOrmModel = self.db.query(UserOrmModel).filter(UserOrmModel.id == userId).first()
        if not userModel:
            AssertTool.raise_biz_with_msg("用户不存在")
        loginUser = self.to_login_user(userModel)
        # 获取当前用户的token
        ext={}
        ext["playerUserId"] = userId
        ext["playerAccount"] = userModel.userName
        ext["isPlayer"] = True
        if loginUser.ext:
            ext = {**loginUser.ext, **ext}
        loginUser.ext = ext
        token = JwtUtil.generate_token(loginUser, AuthService.jwt_secret)
        return LoginToken(token=token, userId=str(userModel.id))

    def un_play_user(self) -> LoginToken:
        """
        获取当前登录用户信息
        :return: 登录用户信息
        """
        loginUser:LoginUser=UserContext.get_current_user()
        playerUserId = loginUser.ext.get("playerUserId")
        userModel: UserOrmModel = self.db.query(UserOrmModel).filter(UserOrmModel.id == playerUserId).first()
        loginUser = self.to_login_user(userModel)
        token = JwtUtil.generate_token(loginUser, AuthService.jwt_secret)
        return LoginToken(token=token, userId=str(userModel.id))

    def to_login_user(self, userModel: UserOrmModel) -> LoginToken:
        """
        把用户实体转换成登录用户

        :param self: 说明
        :param userModel: 用户实体
        :type userModel: UserOrmModel
        :return: 说明
        :rtype: Dict[str, Any]
        """
        permCodes: List[str] = []
        roleList: List[RoleVO] = []
        if userModel.adminType == 1:
            permCodes = ["admin"]
        else:
            # 根据用户id查询其拥有的角色id
            userRoleQuery = self.db.query(UserRoleOrmModel).filter(UserRoleOrmModel.userId == userModel.id)
            userRoleList: List[UserRoleVO] = OrmUtil.to_list(userRoleQuery, UserRoleVO)
            roleIds: List[str] = [userRole.roleId for userRole in userRoleList]
            if roleIds:
                roleQuery = self.db.query(RoleOrmModel).filter(RoleOrmModel.id.in_(roleIds))
                roleList = OrmUtil.to_list(roleQuery, RoleVO)
                # 根据角色ids获取其菜单id
                roleMenuQuery = self.db.query(RoleMenuOrmModel).filter(RoleMenuOrmModel.roleId.in_(roleIds))
                roleMenuList: List[RoleMenuOrmModel] = OrmUtil.to_list(roleMenuQuery, RoleMenuVO)
                menuIds: List[str] = [roleMenu.menuId for roleMenu in roleMenuList]
                if menuIds:
                    # 根据菜单ids获取权限码
                    menuQuery = self.db.query(MenuOrmModel).filter(MenuOrmModel.id.in_(menuIds))
                    permCodes = [menu.code for menu in menuQuery]
        # jwt不建议存放敏感信息，也不建议存放permCodes这种数据长度较长的数据
        # 后续permCodes的数据会存放在redis中，这个等讲到redis的时候再介绍
        loginUser: LoginUser = OrmUtil.to_vo(userModel, LoginUser)
        loginUser.permCodes = permCodes
        loginUser.superAdmin = userModel.adminType == 1
        now = datetime.now()
        loginUser.lastLoginTime = now.strftime("%Y-%m-%d %H:%M:%S")
        # 追加角色信息
        if roleList:
            loginUser.roleIds = [role.id for role in roleList]
            loginUser.roleCodes = [role.code for role in roleList]
            loginUser.roleNames = [role.name for role in roleList]
        # 给登录会话追加postCode、postName、deptCode、deptName信息
        # ===>给后端登录会话用的，比如有些业务需要登录会话中的岗位信息、部门信息
        if userModel.postId:
            post: PostOrmModel = self.db.query(PostOrmModel).filter(PostOrmModel.id == userModel.postId).first()
            if post:
                loginUser.postCode = post.code
                loginUser.postName = post.name
        if userModel.deptId:
            dept: DeptOrmModel = self.db.query(DeptOrmModel).filter(DeptOrmModel.id == userModel.deptId).first()
            if dept:
                loginUser.deptCode = dept.code
                loginUser.deptName = dept.name
        return loginUser
