from unittest import mock

from mat_server.infrastructure.helpers.file_helper import FileHelper


def test_join_file_paths():
    os_module = mock.MagicMock()
    os_module.path.join.return_value = 'join_path'

    codecs_module = mock.MagicMock()
    shutil_module = mock.MagicMock()
    mimetypes_module = mock.MagicMock()
    yaml_module = mock.MagicMock()

    file_helper = FileHelper(
        os_module=os_module,
        codecs_module=codecs_module,
        shutil_module=shutil_module,
        mimetypes_module=mimetypes_module,
        yaml_module=yaml_module,
    )
    assert file_helper.join_file_paths('path1', 'path2') == os_module.path.join.return_value
    os_module.path.join.assert_called_with('path1', 'path2')


def test_guess_file_type():
    os_module = mock.MagicMock()
    codecs_module = mock.MagicMock()
    shutil_module = mock.MagicMock()
    mimetypes_module = mock.MagicMock()
    mimetypes_module.guess_type.return_value = ('type_type', None)
    yaml_module = mock.MagicMock()

    file_helper = FileHelper(
        os_module=os_module,
        codecs_module=codecs_module,
        shutil_module=shutil_module,
        mimetypes_module=mimetypes_module,
        yaml_module=yaml_module,
    )
    assert file_helper.guess_file_type('file_path') == 'type_type'
    mimetypes_module.guess_type.assert_called_with('file_path')


def test_read_bytes():
    data = 'bytes'

    fp = mock.MagicMock()
    fp.read.return_value = data

    os_module = mock.MagicMock()
    codecs_module = mock.MagicMock()
    codecs_module.open.return_value.__enter__.return_value = fp

    shutil_module = mock.MagicMock()
    mimetypes_module = mock.MagicMock()
    yaml_module = mock.MagicMock()

    file_helper = FileHelper(
        os_module=os_module,
        codecs_module=codecs_module,
        shutil_module=shutil_module,
        mimetypes_module=mimetypes_module,
        yaml_module=yaml_module,
    )

    assert file_helper.read_bytes('target_path') == data

    codecs_module.open.assert_called_with('target_path', 'rb')
    fp.read.assert_called_once()


def test_read_yaml():
    fp = mock.MagicMock()
    data = {
        'server': {
            'proxy_url': 'https://paji.marco79423.net',
        },
        'routes': [
            {
                'listen_path': 'demo/hello',
                'query': {
                    'name': '大類',
                },
                'response': {
                    'data': '哈囉 廢物'
                }
            }
        ]
    }

    os_module = mock.MagicMock()
    codecs_module = mock.MagicMock()
    codecs_module.open.return_value.__enter__.return_value = fp

    shutil_module = mock.MagicMock()
    mimetypes_module = mock.MagicMock()

    yaml_module = mock.MagicMock()
    yaml_module.safe_load.return_value = data

    file_helper = FileHelper(
        os_module=os_module,
        codecs_module=codecs_module,
        shutil_module=shutil_module,
        mimetypes_module=mimetypes_module,
        yaml_module=yaml_module,
    )

    assert file_helper.read_yaml('target_path') == data

    codecs_module.open.assert_called_with('target_path', 'r', encoding='utf-8')
    yaml_module.safe_load.assert_called_with(fp)


def test_copy_folder():
    os_module = mock.MagicMock()
    codecs_module = mock.MagicMock()
    shutil_module = mock.MagicMock()
    mimetypes_module = mock.MagicMock()
    yaml_module = mock.MagicMock()

    file_helper = FileHelper(
        os_module=os_module,
        codecs_module=codecs_module,
        shutil_module=shutil_module,
        mimetypes_module=mimetypes_module,
        yaml_module=yaml_module,
    )

    file_helper.copy_folder(
        src_path='src_path',
        dest_path='dest_path',
    )

    shutil_module.copytree.assert_called_with('src_path', 'dest_path')
