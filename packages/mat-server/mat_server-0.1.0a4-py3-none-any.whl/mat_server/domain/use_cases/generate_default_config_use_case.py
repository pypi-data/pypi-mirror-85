from mat_server.domain import base_types, helpers


class GenerateDefaultConfigUseCase(base_types.UseCase):

    def __init__(self,
                 file_helper: helpers.FileHelperBase,
                 project_data_helper: helpers.ProjectDataHelperBase):
        self._file_helper = file_helper
        self._project_data_helper = project_data_helper

    def execute(self):
        # 取得預設設定檔的路徑
        default_mat_data_path = self._project_data_helper.get_default_mat_data_path()

        self._file_helper.copy_folder(
            src_path=str(default_mat_data_path),
            dest_path='mat-data'
        )
