from typing import Union
import base64
import random
import string
import uuid as uuid_lib
from io import BytesIO

from captcha.image import ImageCaptcha
from fastapi import APIRouter,Body,Depends,Header
from sqlalchemy.orm import Session


from database import get_session, transactional_session
from App_Demo.auth_middleware import SaCheckPermission, SaMode,SaIgnore
from App_Demo.base import R,CommonResult
from core.constant_context_holder import ConstantContextHolder
from core.ioc_container import get_service
from modules.sys.params.auth_param import LoginParam
from modules.sys.services.config_service import ConfigService
from modules.sys.services.auth_service import AuthService
from modules.sys.vos.auth_vo import LoginToken

tags = ["授权管理"]
router = APIRouter(tags=tags)


def get_auth_service(db: Session = Depends(get_session)) -> AuthService:
    """
    获取权限服务实例的依赖函数
    """
    return AuthService(db)


@router.post("/sys/login", summary="登录", response_model=CommonResult[LoginToken], response_model_exclude_none=True)
@SaIgnore() #跳过权限检查的装饰器
async def config_save(data: LoginParam = Body(description="登录参数"), auth_service: AuthService = Depends(get_auth_service)) -> CommonResult[LoginToken]:
    loginToken: LoginToken = auth_service.login(data)
    # print(f"登录返回 token: {loginToken.token}")
    return R.data(loginToken)

@router.post("/sys/logout", summary="退出", response_model=CommonResult, response_model_exclude_none=True)
@SaIgnore() #跳过权限检查的装饰器
async def logout(authorization:Union[str,None] = Header(None, description="登录凭证"),auth_service: AuthService = Depends(get_auth_service)):
    if authorization:
        auth_service.logout(authorization)
    return R.success()


@router.post("/sys/getCaptchaOpenFlag", summary="获取是否启用图片验证码标识", response_model=CommonResult[dict], response_model_exclude_none=True)
@SaIgnore()
async def get_captcha_open_flag():
    flag = ConstantContextHolder.get_captcha_open_flag()
    return R.data({
        "flag": flag
    })

@router.post("/sys/captcha", summary="生成图片验证码", response_model=CommonResult[dict], response_model_exclude_none=True)
@SaIgnore()
async def captcha(
    width: int = Body(130, embed=True),
    height: int = Body(48, embed=True),
    length: int = Body(4, alias="len", embed=True),
    charType: int = Body(5, embed=True, description="1:默认 2:仅数字 3:仅字母 4:仅大写 5:仅小写 6:数字+大写"),
):
    """生成图片验证码，返回 uuid + base64"""
    # 选字符集
    char_map = {
        1: string.ascii_uppercase + string.digits,
        2: string.digits,
        3: string.ascii_letters,
        4: string.ascii_uppercase,
        5: string.ascii_lowercase,
        6: string.digits + string.ascii_uppercase,
    }
    chars = char_map.get(charType, string.ascii_uppercase + string.digits)
    captcha_text = ''.join(random.choices(chars, k=max(length, 4)))

    # 生成图片
    image_captcha = ImageCaptcha(width=width, height=height)
    img_data: BytesIO = image_captcha.generate(captcha_text)

    # Base64 编码
    img_base64 = base64.b64encode(img_data.getvalue()).decode()
    base64_str = f"data:image/png;base64,{img_base64}"

    # 存入缓存
    uuid_str = uuid_lib.uuid4().hex
    captcha_cache = get_service("CaptchaCache")
    captcha_cache.set(uuid_str, captcha_text)

    return R.data({"uuid": uuid_str, "base64": base64_str})

@router.post("/badgeConfig", summary="获取菜单徽标配置", response_model=CommonResult, response_model_exclude_none=True)
async def badge_config():

    return R.data([])


@router.post("/sys/playUser", summary="扮演用户", response_model=CommonResult[LoginToken], response_model_exclude_none=True)
@SaCheckPermission("sys:playUser")
async def play_user(data: dict = Body(description="扮演用户"), auth_service: AuthService = Depends(get_auth_service)):
    loginToken: LoginToken = auth_service.play_user(data['userId'])
    return R.data(loginToken)

@router.post("/sys/unPlayUser", summary="取消扮演用户", response_model=CommonResult[LoginToken], response_model_exclude_none=True)
@SaCheckPermission(["sys:playUser","sys:unPlayUser"],mode=SaMode.OR)
async def un_play_user(auth_service: AuthService = Depends(get_auth_service)):
    loginToken: LoginToken = auth_service.un_play_user()
    return R.data(loginToken)

