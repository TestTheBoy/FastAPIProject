#服务层/用户管理控制器封装
from fastapi import APIRouter, Body, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from App_Demo.base import CommonResult, IdParam, IdsParam, CommonPage,R
from App_Demo.user_context import UserContext

from database import get_session, transactional_session
from modules.sys.params.user_role_param import GrantUserRoleParam
from modules.sys.services.user_service import UserService
from modules.sys.params.user_param import UpdateUserAvatarParam, UpdateUserInfoParam, UpdateUserpwdParam, UserParam, UserPageParam
from modules.sys.vos.auth_vo import LoginUser
# from modules.sys.vos.dict_vo import LabelValueVO
from modules.sys.vos.user_vo import UserVO
from core.permission import SaCheckPermission, SaIgnore
from core.permission import SaMode
router = APIRouter(tags=["用户管理"],prefix="")

def get_user_service(db: Session = Depends(get_session)):
    return UserService(db)

@router.post("/sys/user/save",tags=["用户管理"],summary="添加用户",response_model=CommonResult)
async def user_save(param: UserParam=Body(),user_service: UserService = Depends(get_user_service)):
    user_service.save(param)
    return R.success()

@router.post("/sys/user/update",tags=["用户管理"],summary="修改用户",response_model=CommonResult)
async def user_update(param: UserParam=Body(),user_service: UserService = Depends(get_user_service)):
    user_service.update(param)
    return R.success()

@router.post("/sys/user/detail",tags=["用户管理"],summary="用户详情",response_model=CommonResult[UserVO],response_model_exclude_none=True) #response_model_exclude_none:排除空值字段
@SaCheckPermission(["sys:user:detail","sys:user:update"],mode=SaMode.OR)
async def user_detail(param: IdParam=Body(),user_service: UserService = Depends(get_user_service)):
    userVO = user_service.detail(param.id)
    return CommonResult[UserVO](code=0,msg="成功",data=userVO)

@router.post("/sys/user/remove",tags=["用户管理"],summary="用户删除",response_model=CommonResult)
async def user_remove(param: IdsParam=Body(),user_service: UserService = Depends(get_user_service)):
    user_service.removeByIds(param.ids)
    return R.success()

# @router.post("/sys/user/page",tags=["用户管理"],summary="用户分页查询用户列表",response_model=CommonResult[CommonPage[UserVO]])
# async def user_page(param: BasePageParam=Body(),db: Session = Depends(get_session)):
#     result: CursorResult = db.exec("select count(*) from sys_user  limit 0,3")
#     print(result.one()[0])
#
#     return CommonResult[CommonPage[UserVO]](code=0,msg="成功",data=None)

@router.post("/sys/user/page", tags=["用户管理"], summary="用户分页查询用户列表",response_model=CommonResult[CommonPage[UserVO]],response_model_exclude_none=True)
@SaCheckPermission("sys:user:page")
async def user_page(param: UserPageParam = Body(), user_service: UserService = Depends(get_user_service)):
    page = user_service.page(param)
    return CommonResult(code=0,msg="成功",data=page)

@router.post("/sys/user/resetPassword",summary="重置用户密码",response_model=CommonResult,response_model_exclude_none=True)
@SaCheckPermission("sys:user:resetPassword")
async def reset_password(param: IdsParam = Body(), user_service: UserService = Depends(get_user_service)):
    with transactional_session(user_service.db):
        user_service.reset_password(param.ids)
    return R.success()

@router.post("/sys/user/locked", summary="锁定用户", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:user:locked")
async def locked(param: IdsParam = Body(), user_service: UserService = Depends(get_user_service)):
    with transactional_session(user_service.db):
        user_service.locked(param.ids)
    return R.success()

@router.post("/sys/user/unLocked", summary="取消锁定用户", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:user:unLocked")
async def un_locked(param: IdsParam = Body(), user_service: UserService = Depends(get_user_service)):
    with transactional_session(user_service.db):
        user_service.un_locked(param.ids)
    return R.success()
@router.post("/sys/user/info", summary="获取用户信息", response_model=CommonResult[LoginUser], response_model_exclude_none=True)
async def user_info(request: Request, user_service: UserService = Depends(get_user_service)):
    data = user_service.info(request)
    return R.data(data)

@router.post("/sys/user/permCode", summary="获取用户权限码", response_model=CommonResult[List[str]], response_model_exclude_none=True)
async def user_permCode():
    user:LoginUser = UserContext.get_current_user()
    return R.data(user.permCodes)

# @router.post("/sys/user/select", summary="用户下拉数据", response_model=CommonResult[List[LabelValueVO]], response_model_exclude_none=True)
# async def user_select(param: UserPageParam = Body(), user_service: UserService = Depends(get_user_service)):
#     users:List[UserVO] = user_service.list(param)
#     res = [LabelValueVO(label=user.realName, value=user.id) for user in users]
#     return R.data(res)

@router.post("/sys/user/grantRole", summary="授权角色", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:user:grantRole")
async def grant_role(param: GrantUserRoleParam = Body(), user_service: UserService = Depends(get_user_service)):
    with transactional_session(user_service.db):
        user_service.grant_role(param.userId,param.roleIdList)
    return R.success()

@router.post("/sys/user/updateInfo", summary="更新当前用户信息", response_model=CommonResult, response_model_exclude_none=True)
async def update_info(data: UpdateUserInfoParam = Body(description="更新用户信息参数"), user_service: UserService = Depends(get_user_service)):
    with transactional_session(user_service.db):
        user_service.update_info(data)
    return R.success()

@router.post("/sys/user/updateAvatar", summary="更新当前用户头像", response_model=CommonResult, response_model_exclude_none=True)
async def update_avatar(data: UpdateUserAvatarParam = Body(description="更新用户头像参数"), user_service: UserService = Depends(get_user_service)):
    with transactional_session(user_service.db):
        data.id = UserContext.get_current_user_id()
        user_service.update_avatar(data)
    return R.success()

@router.post("/sys/user/updatePwd", summary="更新当前用户密码", response_model=CommonResult, response_model_exclude_none=True)
async def update_pwd(data: UpdateUserpwdParam = Body(description="更新用户密码参数"), user_service: UserService = Depends(get_user_service)):
    data.id = UserContext.get_current_user_id()
    with transactional_session(user_service.db):
        user_service.update_pwd(data)
    return R.success() 