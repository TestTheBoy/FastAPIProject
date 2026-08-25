from fastapi import UploadFile, HTTPException
from PIL import Image
import io

# 规避文件上传时的安全问题，提供通用的文件校验方法
class FileValidator:
    @staticmethod
    def validate_image(file: UploadFile, max_size_mb: int = 2):
        """通用图片校验：检查大小、是否可打开，返回PIL对象供上层复用"""
        contents = file.file.read()
        if len(contents) > max_size_mb * 1024 * 1024:
            raise HTTPException(400, f"文件大小不能超过 {max_size_mb}MB")
        file.file.seek(0)

        try:
            img = Image.open(io.BytesIO(contents))
            img.verify()
            # 重新打开返回对象，以便上层获取宽高
            img = Image.open(io.BytesIO(contents))
            return img, contents
        except Exception:
            raise HTTPException(400, "无效的图片文件")
