import pathlib
from unittest import mock

from mat_server.domain import helpers
from mat_server.domain.use_cases import GenerateDefaultConfigUseCase


def test_generate_default_config():
    project_data_helper = mock.MagicMock(spec=helpers.ProjectDataHelperBase)
    project_data_helper.get_default_mat_data_path.return_value = pathlib.Path('default_mat_data_path')

    file_helper = mock.MagicMock(spec=helpers.FileHelperBase)

    uc = GenerateDefaultConfigUseCase(
        project_data_helper=project_data_helper,
        file_helper=file_helper,
    )

    uc.execute()

    project_data_helper.get_default_mat_data_path.assert_called_once()
    file_helper.copy_folder.assert_called_once_with(
        src_path=str(project_data_helper.get_default_mat_data_path.return_value),
        dest_path='mat-data'
    )
