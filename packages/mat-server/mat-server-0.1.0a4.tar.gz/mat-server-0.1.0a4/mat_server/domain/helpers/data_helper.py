import abc
import pathlib

from mat_server.domain import base_types


class ProjectDataHelperBase(base_types.Helper):

    @abc.abstractmethod
    def get_default_mat_data_path(self) -> pathlib.Path:
        """取得預設設定檔的路徑"""
        pass
