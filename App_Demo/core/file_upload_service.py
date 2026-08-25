

import os
from typing import BinaryIO
import uuid

from fastapi import UploadFile


class FileUploadService:
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

    def save_file(self, file: UploadFile) -> str:
        # 生成唯一的文件名
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(self.upload_dir, unique_filename)

        # 保存文件到指定目录
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        return unique_filename
    
    def upload_file(self, file: BinaryIO, original_filename: str,object_type:str = "default", path_prefix: str = "",kwargs=None) -> str:
        return self.save_file(file)
