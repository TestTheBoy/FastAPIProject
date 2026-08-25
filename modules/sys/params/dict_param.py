from pydantic import BaseModel, Field
from typing import List, Optional


from App_Demo.base import BasePageParam


class DictParam(BaseModel):
    id: Optional[str] = Field(None, title="主键", description="主键")

    
    
    name: str = Field(..., title="字典名称", description="字典名称")
    
    code: str = Field(..., title="唯一编码", description="唯一编码")
    
    groupCode: str = Field(..., title="分组编码", description="分组编码")
    
    sort: Optional[str] = Field(None, title="排序", description="排序")
    
    enabled: Optional[int] = Field(None, title="是否启用", description="是否启用")
    
    dataType: Optional[int] = Field(None, title="数据类型（1：字符串；2：整型）", description="数据类型（1：字符串；2：整型）")
    
    remark: Optional[str] = Field(None, title="备注", description="备注")
    
    
    
    
    
    


class DictPageParam(BasePageParam):
    m_IN_groupCode: Optional[List[str]] = Field(None, title="分组编码", description="分组编码")
    m_LIKE_name: Optional[str] = Field(None, title="字典名称", description="字典名称")

class DictTypeParam(BaseModel):
    dictType: str = Field(..., title="字典类型", description="字典类型")