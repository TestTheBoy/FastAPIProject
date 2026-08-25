from pydantic import BaseModel, Field
from typing import Optional


from App_Demo.base import BasePageParam


class DeptParam(BaseModel):
    id: Optional[str] = Field(None, title="主键", description="主键")

    
    
    parentId: Optional[str] = Field(None, title="父ID", description="父ID")
    
    pids: Optional[str] = Field(None, title="父ID集合", description="父ID集合")
    
    name: str = Field(..., title="部门名称", description="部门名称")
    
    code: str = Field(..., title="唯一编码", description="唯一编码")
    
    sort: Optional[str] = Field(None, title="排序", description="排序")
    
    enabled: Optional[int] = Field(None, title="是否启用", description="是否启用")
    
    leaderIds: Optional[str] = Field(None, title="部门负责人ID集合", description="部门负责人ID集合")
    
    mainLeaderId: Optional[str] = Field(None, title="分管领导ID", description="分管领导ID")
    
    remark: Optional[str] = Field(None, title="备注", description="备注")
    
    
    
    
    
    


class DeptPageParam(BasePageParam):
    pass