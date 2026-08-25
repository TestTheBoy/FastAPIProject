
import os
from typing import Any, Dict


class ConstantContextHolder:
    def __init__(self):
        self.constant_context = {}

    def get_constant_context(self) -> Dict[str, str]:
        return self.constant_context

    @classmethod
    def get_sys_config_with_default(cls, key: str, cast: type = str, default: Any = None) -> Any:
        """从环境变量读取配置，不存在时返回默认值"""
        value = os.environ.get(key)
        if value is None:
            return default
        if cast is bool:
            return value.lower() in ("true", "1", "yes")
        return cast(value)
    
    @classmethod
    def get_sm2_private_key(cls) -> str:
        '''
        获取smm2私钥
        '''
        return cls.get_sys_config_with_default("MOLE_SM2_PRIVATE_KEY", str, "")
    
    @classmethod
    def get_sm2_public_key(cls) -> str:
        '''
        获取sm2公钥
        '''
        return cls.get_sys_config_with_default("MOLE_SM2_PUBLIC_KEY", str, "")
    
    @classmethod
    def get_sm2_open_flag(cls) -> str:
        '''
        是否开启sm2加密(export MOLE_SM2_OPEN_FLAG)
        '''
        return cls.get_sys_config_with_default("MOLE_SM2_OPEN_FLAG", bool, False) 
    
    @classmethod
    def get_captcha_type(cls) -> str:
        '''
        获取验证码uuidkey
        '''
        return cls.get_sys_config_with_default("MOLE_CAPTCHA_UUID_KEY", str, "uuid")

    @classmethod
    def get_cache_key_prefix(cls) -> str:
        """
        获取 Redis 缓存键的系统级前缀

        所有缓存键统一使用此前缀，便于多环境/多应用隔离。
        """
        return cls.get_sys_config_with_default("CACHE_KEY_PREFIX", str, "mldong:")

    @classmethod
    def get_captcha_code_key(cls) -> str:
        '''
        获取验证码codekey
        '''
        return cls.get_sys_config_with_default("MOLE_CAPTCHA_CODE_KEY", str, "code")
    
    @classmethod
    def get_captcha_open_flag(cls) -> str:
        '''
        获取验证码开关
        '''
        return cls.get_sys_config_with_default("MOLE_CAPTCHA_OPEN_FLAG", bool, True)
    
    @classmethod
    def get_upload_base_path(cls) -> str:
        '''
        获取上传文件基础路径
        '''
        return cls.get_sys_config_with_default("UPLOAD_BASE_PATH", str, "")
    
    @classmethod
    def get_img_base_url(cls) -> str:
        '''
        获取图片访问地址
        '''
        return cls.get_sys_config_with_default("IMG_BASE_URL", str, "")
    
    @classmethod
    def get_captcha_expire(cls) -> int:
        '''
        获取验证码过期时间
        '''
        return cls.get_sys_config_with_default("MOLE_CAPTCHA_EXPIRE", int, 300)
    
    @classmethod
    def get_captcha_uuid_key(cls) -> str:
        '''
        获取验证码uuidkey
        '''
        return cls.get_sys_config_with_default("MOLE_CAPTCHA_UUID_KEY", str, "uuid")