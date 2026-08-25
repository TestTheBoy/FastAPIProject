from pydantic import BaseModel, Field
from typing import Optional


from App_Demo.base import BasePageParam


class ConfigParam(BaseModel):
    id: Optional[str] = Field(None, title="主键", description="主键")

    
    
    name: str = Field(..., title="配置名称", description="配置名称")
    
    code: str = Field(..., title="唯一编码", description="唯一编码")
    
    groupCode: str = Field(..., title="分组编码", description="分组编码")
    
    content: Optional[str] = Field(None, title="配置内容", description="配置内容")
    
    isSys: Optional[int] = Field(None, title="是否系统", description="是否系统")
    
    enabled: Optional[int] = Field(None, title="是否启用", description="是否启用")
    
    remark: Optional[str] = Field(None, title="备注", description="备注")
    
    
    
    
    
    


class ConfigPageParam(BasePageParam):
    pass