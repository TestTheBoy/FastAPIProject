from datetime import datetime
import os
import uuid

from fastapi import APIRouter, Body, Depends, File, Form, Request, UploadFile
from sqlalchemy.orm import Session



from App_Demo.util import OrmUtil
# from App_Demo.core.file_upload_service import FileUploadService  # 暂注释，FileUploadService 未就绪
from database import get_session, transactional_session
from App_Demo.auth_middleware import SaCheckPermission, SaMode
from App_Demo.base import R, CommonPage, CommonResult, IdParam, IdsParam

from modules.sys.params.file_info_param import FileInfoPageParam, FileInfoParam
from modules.sys.services.file_info_service import FileInfoService
from modules.sys.vos.file_info_vo import FileInfoVO

try:
    from config import IMG_BASE_URL
except Exception:
    IMG_BASE_URL = "http://localhost:8000/uploadfiles/"

tags = ["文件信息"]
router = APIRouter(tags=tags)


def get_file_info_service(db: Session = Depends(get_session)) -> FileInfoService:
    """
    获取文件信息服务实例的依赖函数
    """
    return FileInfoService(db)


@router.post("/sys/fileInfo/upload", summary="上传文件", response_model=CommonResult, response_model_exclude_none=True)
async def file_info_upload(request: Request, file: UploadFile = File(...), 
                           file_info_service: FileInfoService = Depends(get_file_info_service),
                           persist:int = Form(1, description="是否持久化，1=持久化，0=不持久化"),
                           objectType: str = Form("default",description = "对象类型")):
    '''
    上传文件，成功返回文件 id/url
    :param request: 请求对象
    '''
     # 只做校验，不混杂任何校验代码
    validated_file = FileInfoService.validate_avatar(file)

    # 校验后文件指针已回到开头，直接读取保存
    # 注意：validated_file 和 file 是同一个对象，只读一次
    file_bytes = await validated_file.read()

    # 将文件内容转换为类文件对象（暂注释，FileUploadService 未就绪）
    # from io import BytesIO
    # file_io = BytesIO(file_bytes)
    # file_upload_service: FileUploadService = request.app.state.file_upload_service
    # result = file_upload_service.upload_file(file_io, validated_file.filename, persist=persist, objectType=objectType)
    # 构建文件信息对象
    # file_info_dict = {
    #     
    #     "url": result["url"],
    #     "size": result["size"],
    #     "sizeInfo": result["size_info"],
    #     "fileName": result["file_name"],
    #     "originalFileName": result["original_file_name"],
    #     "ext": result["ext"],
    #     "path": result["path"],
    #     "platform": result["platform"],
    #     "contentType": result["content_type"],
    #     "objectId": OrmUtil.generate_id(),
    #     "objectType": objectType,
    #     "attr" : f"{{'persist': {persist},'ext': '{result['ext']}'}}"
    #     
    # }

    # 数据库持久化先注释掉，后面再补
    # if persist == 1:
    #     with transactional_session(file_info_service.db):
    #         file_info_model = FileInfoParam(**file_info_dict)
    #         file_info_service.db.add(file_info_model)
    
    # with transactional_session(file_info_service.db):
    #     pass
    
    # --- 业务逻辑：生成唯一文件名保存（防止路径遍历攻击）---
    # 不要用用户上传的原始文件名！用 UUID 重命名！
    ext = os.path.splitext(validated_file.filename)[-1]# 获取 .jpg
    safe_filename = f"{uuid.uuid4().hex}{ext}"  # 生成 a1b2c3d4e5f6.jpg
    date_str = datetime.now().strftime("%Y/%m/%d")
    biz_type = objectType  # 业务类型，可根据实际需求修改
    dir_path = os.path.join("uploadfiles", biz_type, date_str)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, safe_filename)
    with open(file_path, "wb") as f: # 上传保存文件
        f.write(file_bytes)

    url = f"{biz_type}/{date_str}/{safe_filename}"
    return R.data({
        "url": url,  #用户提交更新入库
        "fullUrl": f"{IMG_BASE_URL}{url}", #前端预览
    })


@router.post("/sys/fileInfo/update", summary="修改文件信息", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:fileInfo:update")
async def file_info_update(data: FileInfoParam = Body(description="文件信息参数"), file_info_service: FileInfoService = Depends(get_file_info_service)):
    with transactional_session(file_info_service.db):
        file_info_service.update(data)
    return R.success()


@router.post("/sys/fileInfo/remove", summary="删除文件信息", response_model=CommonResult, response_model_exclude_none=True)
@SaCheckPermission("sys:fileInfo:remove")
async def file_info_remove(param: IdsParam = Body(), file_info_service: FileInfoService = Depends(get_file_info_service)):
    with transactional_session(file_info_service.db):
        file_info_service.remove_by_ids(param.ids)
    return R.success()


@router.post("/sys/fileInfo/detail", summary="文件信息详情", response_model=CommonResult[FileInfoVO], response_model_exclude_none=True)
@SaCheckPermission(["sys:fileInfo:detail", "sys:fileInfo:update"], mode=SaMode.OR)
async def file_info_detail(param: IdParam = Body(), file_info_service: FileInfoService = Depends(get_file_info_service)):
    data = file_info_service.detail(param.id)
    return R.data(data)


@router.post("/sys/fileInfo/page", summary="分页查询文件信息列表", response_model=CommonResult[CommonPage[FileInfoVO]], response_model_exclude_none=True)
@SaCheckPermission("sys:fileInfo:page")
async def file_info_page(param: FileInfoPageParam = Body(), file_info_service: FileInfoService = Depends(get_file_info_service)):
    data = file_info_service.page(param)
    return R.data(data)
