from abc import ABC, abstractmethod
import logging
from typing import BinaryIO,Dict,Any, List


class FileStorage(ABC):
    '''
    文件存储策略抽象基类
    '''

    @abstractmethod
    def upload(self, file: BinaryIO, file_name: str,path: str,**kwargs) -> Dict[str, Any]:
        """
        上传文件
        :param file: 文件对象
        :param file_name: 文件名
        :param path: 文件存储路径
        :param kwargs: 其他参数
        :return: 返回上传结果，包含文件的URL、大小、类型等信息
        """
        pass

    @abstractmethod
    def download(self, file_url: str) -> bytes:
        """
        下载文件
        :param file_url: 文件的URL
        :return: 返回文件对象
        """
        pass

    @abstractmethod
    def delete(self, file_url: str) -> bool:
        """
        删除文件
        :param file_url: 文件的URL
        :return: 删除成功返回True，否则返回False
        """
        pass

    @abstractmethod
    def get_url(self, file_url: str) -> str:
        """
        获取文件的访问URL
        :param file_url: 文件的URL
        :return: 返回文件的访问URL
        """
        pass

    def initiate_multipart_upload(self, file_name: str, path: str, **kwargs) -> Dict[str, Any]:
        """
        初始化分片上传
        :param file_name: 文件名
        :param path: 文件存储路径
        :param kwargs: 其他参数
        :return: 返回初始化结果，包含上传ID、分片大小等信息
        """
        raise NotImplementedError("该存储类型不支持分片上传")
    
    def upload_part(self, file: BinaryIO, upload_id: str, part_number: int, **kwargs) -> Dict[str, Any]:
        """
        上传分片
        :param file: 文件对象
        :param upload_id: 上传ID
        :param part_number: 分片编号
        :param kwargs: 其他参数
        :return: 返回上传结果，包含分片URL、大小等信息
        """
        raise NotImplementedError("该存储类型不支持分片上传")
    
    def complete_multipart_upload(self, upload_id: str, parts: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """
        完成分片上传
        :param upload_id: 上传ID
        :param parts: 分片列表
        :param kwargs: 其他参数
        :return: 返回完成结果，包含文件的URL、大小、类型等信息
        """
        raise NotImplementedError("该存储类型不支持分片上传")
    
    def abort_multipart_upload(self, upload_id: str, **kwargs) -> bool:
        """
        取消分片上传
        :param upload_id: 上传ID
        :param kwargs: 其他参数
        :return: 取消成功返回True，否则返回False
        """
        raise NotImplementedError("该存储类型不支持分片上传")
    
    # def save_file_part(self, file_part_detail:FilePartDetail) -> bool:
    #     """
    #     保存分片文件
    #     :param file_part_detail: 分片文件详情
    #     :return: 存储结果
    #     """
    # try:
    #     file_part_cache : FilePartCache = get_service(FilePartCache)
    # except Exception as e:
    #     logging.error(f"获取FilePartCache服务失败: {e}")
    #     raise RuntimeError("获取FilePartCache服务失败")
    #   return self.upload_part(file_part_detail.file, file_part_detail.upload_id, file_part_detail.part_number)
