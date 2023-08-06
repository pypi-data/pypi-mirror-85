import pathlib

from mat_server.infrastructure.helpers import ProjectDataHelper


def test_get_default_mat_data_path():
    project_data_helper = ProjectDataHelper(
        data_dir=pathlib.Path('.')
    )
    assert project_data_helper.get_default_mat_data_path() == pathlib.Path('.') / 'default' / 'mat-data'
