"""
是/否枚举

遵循企业级惯例：
    - Yes (0)：正常 / 是 / 未删除
    - No  (1)：禁用 / 否 / 已删除

数据库整数字段默认值为 0，因此 Yes 对应 0 可与数据库默认值保持一致。
"""

from enum import Enum


class YesNoEnum(Enum):
    """
    通用是/否枚举

    使用示例::

        # 查询未删除的记录
        query.filter(Model.deleted == YesNoEnum.Yes.code)

        # 判断是否禁用
        if record.status == YesNoEnum.No.code:
            raise Exception("已禁用")
    """

    Yes = (0, "是")
    No = (1, "否")

    def __new__(cls, code: int, label: str):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.code = code
        obj.label = label
        return obj

    @classmethod
    def of(cls, code: int) -> "YesNoEnum":
        """根据 code 获取枚举实例"""
        for member in cls:
            if member.code == code:
                return member
        return None
