import hashlib
import random
import re
import string
from typing import Optional, Type, Callable, Any, Union, TypeVar, List

from overrides.typing_utils import get_origin
from sqlalchemy.orm import Query
from typing_extensions import get_args
from core.snawflake_id_generator import SnowflakeIDGenerator
from modules.sys.vos.auth_vo import LoginToken,LoginUser
import jwt
import datetime
from typing import Optional, Dict, Any

T = TypeVar('T')

class StrUtil:
    """
    字符串工具类
    """

    @staticmethod
    def hump_to_underline(text):
        """
        驼峰转下划线
        :param text:
        :return:
        """
        res = []
        for index, char in enumerate(text):
            if char.isupper() and index != 0:
                 res.append("_")
            res.append(char)
        return "".join(res).lower()

    @staticmethod
    def underline_to_hump(text):
        """
        下划线转大驼峰
        :param text:
        :return:
        """
        arr = text.lower().split("_")
        res = []
        for i in arr:
            res.append(i[0].upper() + i[1:])
        return "".join(res)

    @staticmethod
    def underline_to_camel(text):
        """
        下划线转小驼峰
        :param text:
        :return:
        """
        s = StrUtil.underline_to_hump(text)
        return s[0].lower() + s[1:]

    @staticmethod
    def camel_to_hump(text):
        """
        小驼峰转大驼峰
        :param text: 小驼峰格式的字符串
        :return: 大驼峰格式的字符串
        """
        if not text:
            return text
        return text[0].upper() + text[1:]

    @staticmethod
    def hump_to_camel(text):
        """
        大驼峰转小驼峰
        :param text: 大驼峰格式的字符串
        :return: 小驼峰格式的字符串
        """
        if not text:
            return text
        return text[0].lower() + text[1:]

    @staticmethod
    def md5_encrypt(string):
        # 创建一个md5 hash对象
        m = hashlib.md5()

        # 必须使用encode()函数对字符串进行编码，否则会抛出TypeError异常
        m.update(string.encode("utf-8"))

        # 使用hexdigest()函数获取加密后的16进制结果
        return m.hexdigest()

    @staticmethod
    def random_string(len):
        """
        生成随机字符串
        """

        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(len)
        )

    @staticmethod
    def ant_matcher(request_path, pattern):
        """
        Ant风格路径匹配
        """
        parts = pattern.split("/")
        matcher = re.compile(
            "^"
            + "/".join(
                [
                    re.escape(part).replace("\\*", ".*").replace("\\**", "(/.*)?")
                    for part in parts
                ]
            )
            + "$"
        )
        return bool(matcher.match(request_path))

    @staticmethod
    def extract_fields(original_dict, field_names_str):
        """
        从原始字典中提取指定字段名的值，并返回一个新字典。

        :param original_dict: 包含所有数据的原始字典
        :param field_names_str: 字符串，包含以逗号分隔的需要提取的字段名
        :return: 一个新字典，包含提取的字段名及其对应的值
        """
        # 创建一个空字典用于存放提取的字段
        extDict = {}
        if field_names_str is None or field_names_str == "":
            return extDict
        # 分割字符串以获取字段名列表
        field_names = field_names_str.split(",")

        # 遍历字段名列表，从原始字典中提取值
        for field_name in field_names:
            # 如果字段名在原始字典中，则添加到extDict字典中
            if field_name in original_dict:
                extDict[field_name] = original_dict[field_name]

        return extDict

class OrmUtil:
    """
    ORM工具类
    """

    @staticmethod
    def to_vo(ormObj, vo_class: Optional[Type[T]] = None, row_handler: Optional[Callable[[Any], T]] = None) -> Union[
        T, Any, None]:
        """
        将orm对象转为vo对象
        :param ormObj: orm对象
        :param vo_class: vo类
        :param row_handler: 后置处理函数，可以给vo_class追加额外属性或二次处理
        :return: 转换后的vo对象
        """

        # 处理空对象情况
        if ormObj is None:
            return None

        # 如果没有指定vo_class，则直接返回原始对象
        if vo_class is None:
            return ormObj

        # 构建传递给 vo_class 的字段字典
        vo_data = {}
        ormDict = {}
        if hasattr(ormObj, "__dict__"):
            # orm 对象
            for key, value in ormObj.__dict__.items():
                # 过滤掉 SQLAlchemy 的内部属性
                if not key.startswith('_'):
                    ormDict[key] = value
        if hasattr(ormObj, "_asdict"):
            # Row 对象
            asdict = ormObj._asdict()
            for key, value in asdict.items():
                if value and hasattr(value, "__dict__"):
                    for k, v in value.__dict__.items():
                        if not k.startswith('_'):
                            ormDict[k] = v
                else:
                    if not key.startswith('_'):
                        ormDict[key] = value

        fieldKeys = ormDict.keys()
        # 遍历 vo_class 的所有字段
        for field_name, field_info in vo_class.model_fields.items():
            # 检查 ORM 对象是否有对应属性
            if field_name in fieldKeys:
                field_value = ormDict[field_name]
            else:
                # 特殊字段映射：userId <- id
                if field_name == 'userId' and 'id' in fieldKeys:
                    field_value = ormDict['id']
                else:
                    # 尝试驼峰转下划线：userName -> username
                    snake_case = ''.join(['_' + c.lower() if c.isupper() else c for c in field_name]).lstrip('_')
                    if snake_case in fieldKeys:
                        field_value = ormDict[snake_case]
                    else:
                        continue  # 如果找不到对应字段，跳过

            # 处理类型转换，特别是 Union 类型中包含 str 的情况
            origin_type = get_origin(field_info.annotation)
            if origin_type is not None and origin_type is Union:
                # 如果字段类型是 Union 且包含 str，则将值转换为字符串
                if str in get_args(field_info.annotation) and field_value is not None:
                    field_value = str(field_value)
            else:
                if field_info.annotation is str and field_value is not None:
                    field_value = str(field_value)

            vo_data[field_name] = field_value

        # 创建VO对象
        try:
            vo_instance = vo_class(**vo_data)
        except Exception as e:
            raise ValueError(f"Failed to create VO instance: {e}")

        # 应用后置处理函数（如果提供）
        if row_handler is not None:
            try:
                vo_instance = row_handler(vo_instance)
            except Exception as e:
                raise ValueError(f"Error in row_handler: {e}")

        return vo_instance

    @classmethod
    def has_logic_delete_field(cls):
        """
        判断模型实例是否存在逻辑删除字段且未被设置为None
        :param cls: 模型类
        :return: bool
        """
        # 检查模型是否有isDeleted属性，且该属性不为None
        # 如果属性为None，表示该字段在当前模型中被显式设置为不映射
        return (
                hasattr(cls, 'isDeleted')
                and getattr(cls, 'isDeleted') is not None
        )

    @staticmethod
    def to_list(query: Query, vo_class=None, row_handler: Optional[Callable[[Any], T]] = None) -> List[T]:
        """
        将SQLAlchemy查询对象转成vo-list
        :param query: SQLAlchemy查询对象
        :param vo_class: VO类，用于转换模型对象
        :param row_handler: 行处理函数，用于处理每一行数据
        :return: List[VO] 列表对象
        """
        items = query.all()
        # 转换为VO对象
        rows = []
        for item in items:
            obj = OrmUtil.to_vo(item, vo_class, row_handler)
            if obj is not None:
                rows.append(obj)
        return rows

    @staticmethod
    def generate_id():
        id = SnowflakeIDGenerator.generate_id() # 利用雪花算法生成id
        print("Generated ID : %s",id)
        return id





class JwtUtil:
    """
    JWT工具类，用于生成和验证JWT令牌
    """

    @staticmethod
    def generate_token(loginUser: LoginUser, secret_key: str, expires_in: int = 3600) -> str:
        """
        生成JWT令牌

        :param payload: 要包含在令牌中的数据
        :param secret_key: 用于签名的密钥
        :param expires_in: 令牌过期时间（秒），默认1小时
        :return: JWT令牌字符串
        """
        if isinstance(loginUser, dict):
            payload = loginUser.copy()
        else:
            payload = loginUser.model_dump()
        # payload = loginUser.model_dump()
        # 添加过期时间
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)

        # 生成JWT令牌
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token

    @staticmethod
    def verify_token(token: str, secret_key: str) -> Optional[LoginUser]:
        """
        验证JWT令牌
 **
        :param token: JWT令牌字符串
        :param secret_key: 用于验证签名的密钥
        :return: 解码后的令牌数据，如果验证失败则返回None
        """
        try:
            # 验证并解码JWT令牌
            decoded_payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            # 确保 userId 是字符串类型（JWT 解码后数字会变成 int）
            if 'userId' in decoded_payload and not isinstance(decoded_payload['userId'], str):
                decoded_payload['userId'] = str(decoded_payload['userId'])

            return LoginUser(**decoded_payload)
        except jwt.ExpiredSignatureError:
            # 令牌已过期
            return None
        except jwt.InvalidTokenError:
            # 令牌无效
            return None

    @staticmethod
    def get_payload(token: str, secret_key: str) -> Optional[LoginUser]:
        """
        获取JWT令牌中的载荷数据，不验证过期时间

        :param token: JWT令牌字符串
        :param secret_key: 用于验证签名的密钥
        :return: 令牌中的载荷数据，如果解析失败则返回None
        """
        try:
            # 解码JWT令牌，不验证过期时间
            decoded_payload = jwt.decode(token, secret_key, algorithms=['HS256'], options={"verify_exp": False})
            if 'userId' in decoded_payload and not isinstance(decoded_payload['userId'], str):
                decoded_payload['userId'] = str(decoded_payload['userId'])

            return LoginUser(**decoded_payload)
        except jwt.InvalidTokenError:
            # 令牌无效
            return None


class TreeUtil:
    """
    树结构工具类
    """

    @staticmethod
    def build_tree(nodes_list, parent_id: str = "0"):
        """
        构建树，parent_id默认为0
        """
        return TreeUtil._build_tree(nodes_list=nodes_list, parent_id=parent_id)

    @staticmethod
    def _build_tree(nodes_list, parent_id):
        """
        递归构建树结构
        """
        if nodes_list is None or len(nodes_list) == 0:
            return []
        children = []
        for node in nodes_list:
            # 获取节点的parentId，支持dict和pydantic模型
            if hasattr(node, 'parentId'):
                node_parent_id = node.parentId
            elif isinstance(node, dict) and 'parentId' in node:
                node_parent_id = node['parentId']
            else:
                continue
            if str(node_parent_id) == str(parent_id):
                children.append(node)
                # 获取节点的id，支持dict和pydantic模型
                if hasattr(node, 'id'):
                    node_id = node.id
                elif isinstance(node, dict) and 'id' in node:
                    node_id = node['id']
                else:
                    continue

                node_children = TreeUtil._build_tree(nodes_list, node_id)
                if len(node_children) > 0:
                    if hasattr(node, 'children'):
                        node.children = node_children
                    elif isinstance(node, dict):
                        node['children'] = node_children
        return children
