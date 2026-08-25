

import base64
from io import BytesIO
import random
import string
from typing import Optional
from PIL import Image
from fastapi import Request
import redis
from App_Demo.query_param_context import QueryParamContext
from App_Demo.core.constant_context_holder import ConstantContextHolder
from App_Demo.core.exception import AssertTool
from App_Demo.core.middleware.query_param_context import RequestContext
from App_Demo.core.ioc_container import get_service

class CaptchaService:
     # 定义字符类型常量
    TYPE_NUM_ONLY = "number"
    TYPE_CHAR_ONLY = "char"
    TYPE_MIX = "mix"
    def _generate_captcha(self,width:int,height:int,length:int,char_type:str):
        """
        生成验证码
        :param width: 验证码宽度
        :param height: 验证码高度
        :param len: 验证码长度
        :param char_type: 验证码类型
        :return: 验证码文本，baser64图片
        """
        #设置实际尺寸（比默认更大，提升可读性
        width = width or 160
        height = height or 60
        length = length or 5
        
        #获取验证码生成器
        image_captcha = self._generate_captcha(width=width, height=height)

        #生成验证码文本
        
        if char_type == self.TYPE_NUM_ONLY:
            chars = string.digits
        elif char_type == self.TYPE_CHAR_ONLY:
            chars = string.ascii_uppercase
        else:
            chars = string.ascii_uppercase + string.digits
        
        captcha_text = ''.join(random.choices(chars, k=length))  # 用 choices 允许重复

        #生成图像数据
        data = image_captcha.generate(chars = captcha_text,bg_color=(255,255,255,0))

        #将图像数据写入 BytesIO
        buffered = BytesIO()
        data.seek(0) #回到开头
        buffered.write(data.read()) #写入缓冲区
        buffered.seek(0) #回到开头

        #使用PIL 打开并保存为PNG
        image = Image.open(buffered)
        imag_buffer = BytesIO()
        image.save(imag_buffer, format='PNG')
        imag_buffer.seek(0)

        #编码为base64
        imge_base64 = base64.b64encode(imag_buffer.getvalue()).decode()
        base64_str = f"data:image/png;base64,{imge_base64}"

        return captcha_text,base64_str
        
    def validate(self, uuid: str=None, code: str=None, is_remove_when_success=True) -> bool:
        '''
        验证码验证
        :param uuid:验证码uuid
        :param code:验证码
        :param is_remove_when_success:验证成功时是否删除验证码
        :return:验证结果
        '''
        uuidkey = ConstantContextHolder.get_captcha_uuid_key()
        codekey = ConstantContextHolder.get_captcha_code_key()
        request : Request = RequestContext.get_request()

        #如果uuid 或code为空,则尝试从请求头或请求体中获取
        if request:
            #从请求头中获取
            if not uuid:
                
                uuid = request.headers.get(uuidkey) or request.query_params.get(uuidkey) or  QueryParamContext.get_current_query_params().get(uuidkey)
            if not code:
                code = request.headers.get(uuidkey) or QueryParamContext.get_current_query_params().get(codekey) or request.query_params.get(codekey) 

        #校验参数
        if not uuid or not code:
            return False

        captcha_code :CaptchaCache = get_service("CaptchaCache")
        cached_code = captcha_code.get(uuid)
        if not cached_code:
            return False
        flag = str(code).lower() == str(cached_code).lower()
        if flag and is_remove_when_success:
            captcha_code.remove(uuid)

        return flag
    
from App_Demo.core.redis_cache_operator import AbstractRedisCacheOperator


class CaptchaCache(AbstractRedisCacheOperator[str]):
    """
    验证码缓存，基于 Redis 存储，Redis 不可用时自动降级为内存字典

    继承自 AbstractRedisCacheOperator，复用 Redis 连接的获取、序列化等通用逻辑。
    """

    def __init__(self, redis_client: Optional[redis.Redis] = None):
        super().__init__(
            redis_client=redis_client,
            model_class=None,
            key_prefix="captcha:"
        )

    # get / set / remove / exists 已由 AbstractRedisCacheOperator 提供默认实现，
    # 此处无需重写。验证码为纯字符串，序列化/反序列化均为透传。
    #
    # 如需自定义过期时间等行为，可覆盖父类方法。