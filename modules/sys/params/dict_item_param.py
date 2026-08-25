from pydantic import BaseModel, Field
from typing import Optional


from App_Demo.base import BasePageParam


class DictItemParam(BaseModel):
    id: Optional[str] = Field(None, title="主键", description="主键")

    
    
    dictId: str = Field(..., title="字典ID", description="字典ID")
    
    name: str = Field(..., title="字典项名称", description="字典项名称")
    
    code: str = Field(..., title="唯一编码", description="唯一编码")
    
    sort: Optional[str] = Field(None, title="排序", description="排序")
    
    enabled: Optional[int] = Field(None, title="是否启用", description="是否启用")
    
    remark: Optional[str] = Field(None, title="备注", description="备注")
    
    
    
    
    
    


class DictItemPageParam(BasePageParam):
    M_EQ_dictId: Optional[str] = Field(None, title="字典ID", description="字典ID")
    m_LIKE_name: Optional[str] = Field(None, title="字典项名称", description="字典项名称")
    m_LIKE_code: Optional[str] = Field(None, title="唯一编码", description="唯一编码")