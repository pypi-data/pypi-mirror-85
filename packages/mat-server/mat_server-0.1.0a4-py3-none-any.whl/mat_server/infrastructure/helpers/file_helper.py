from typing import Any
import mimetypes

from mat_server.domain import helpers


class FileHelper(helpers.FileHelperBase):

    def __init__(self,
                 os_module,
                 codecs_module,
                 shutil_module,
                 mimetypes_module,
                 yaml_module):
        self._os_module = os_module
        self._codecs_module = codecs_module
        self._shutil_module = shutil_module
        self._mimetypes_module = mimetypes_module
        self._yaml_module = yaml_module

    def join_file_paths(self, *paths: str) -> str:
        return self._os_module.path.join(*paths)

    def guess_file_type(self, path: str) -> str:
        """猜測檔案類型"""
        return self._mimetypes_module.guess_type(path)[0]

    def read_bytes(self, target_path: str) -> bytes:
        """讀取檔案資料"""
        with self._codecs_module.open(target_path, 'rb') as fp:
            return fp.read()

    def read_yaml(self, target_path: str) -> Any:
        """讀取 yaml 檔案"""
        with self._codecs_module.open(target_path, 'r', encoding='utf-8') as fp:
            return self._yaml_module.safe_load(fp)

    def copy_folder(self, src_path: str, dest_path: str):
        """複製資料夾 (支援遞迴複製)"""
        self._shutil_module.copytree(src_path, dest_path)
