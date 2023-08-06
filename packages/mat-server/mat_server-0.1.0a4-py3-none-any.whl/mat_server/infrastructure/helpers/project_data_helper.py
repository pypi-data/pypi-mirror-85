import pathlib

from mat_server.domain import helpers

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / 'data'


class ProjectDataHelper(helpers.ProjectDataHelperBase):

    def __init__(self,
                 data_dir: pathlib.Path = DATA_DIR):
        self._data_dir = data_dir

    def get_default_mat_data_path(self) -> pathlib.Path:
        """取得預設設定檔的路徑"""
        return self._data_dir / 'default' / 'mat-data'
