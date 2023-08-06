from unittest import mock

import fastapi

from mat_server.app.manager import Manager
from mat_server.app.server import Server
from mat_server.domain import use_cases, entities


def test_create_config(capsys):
    generate_default_config_use_case = mock.MagicMock(spec=use_cases.GenerateDefaultConfigUseCase)
    check_config_use_case = mock.MagicMock(spec=use_cases.CheckConfigUseCase)
    server = mock.MagicMock(spec=Server)

    manager = Manager(
        generate_default_config_use_case=generate_default_config_use_case,
        check_config_use_case=check_config_use_case,
        server=server,
    )

    manager.create_config()

    captured = capsys.readouterr()
    assert captured.out == '初始化 mat 設定 ...\nmat-data 資料夾建立完成\n'
    generate_default_config_use_case.execute.assert_called_once()


def test_check_failed(capsys):
    generate_default_config_use_case = mock.MagicMock(spec=use_cases.GenerateDefaultConfigUseCase)

    check_config_use_case = mock.MagicMock(spec=use_cases.CheckConfigUseCase)
    check_config_use_case.execute.return_value = entities.ValidationReport(
        failed_reasons=['必須要有 proxy host 設定']
    )

    server = mock.MagicMock(spec=Server)

    manager = Manager(
        generate_default_config_use_case=generate_default_config_use_case,
        check_config_use_case=check_config_use_case,
        server=server,
    )

    assert manager.check_config() is False

    check_config_use_case.execute.assert_called_once()

    captured = capsys.readouterr()
    assert captured.out == '檢查設定檔 ...\n[x] 必須要有 proxy host 設定\n設定檔設定錯誤\n'


def test_check_success(capsys):
    generate_default_config_use_case = mock.MagicMock(spec=use_cases.GenerateDefaultConfigUseCase)

    check_config_use_case = mock.MagicMock(spec=use_cases.CheckConfigUseCase)
    check_config_use_case.execute.return_value = entities.ValidationReport()

    server = mock.MagicMock(spec=Server)

    manager = Manager(
        generate_default_config_use_case=generate_default_config_use_case,
        check_config_use_case=check_config_use_case,
        server=server,
    )

    manager.check_config()

    check_config_use_case.execute.assert_called_once()

    captured = capsys.readouterr()
    assert captured.out == '檢查設定檔 ...\n設定檔檢查完成\n'


def test_serve_failed(capsys):
    generate_default_config_use_case = mock.MagicMock(spec=use_cases.GenerateDefaultConfigUseCase)

    check_config_use_case = mock.MagicMock(spec=use_cases.CheckConfigUseCase)
    check_config_use_case.execute.return_value = entities.ValidationReport(
        failed_reasons=['必須要有 proxy host 設定']
    )

    server = mock.MagicMock(spec=Server)

    manager = Manager(
        generate_default_config_use_case=generate_default_config_use_case,
        check_config_use_case=check_config_use_case,
        server=server,
    )

    manager.serve('0.0.0.0', port=9527)

    check_config_use_case.execute.assert_called_once()

    captured = capsys.readouterr()
    assert captured.out == '檢查設定檔 ...\n[x] 必須要有 proxy host 設定\n設定檔設定錯誤\n'


def test_get_server_api_router():
    generate_default_config_use_case = mock.MagicMock(spec=use_cases.GenerateDefaultConfigUseCase)
    check_config_use_case = mock.MagicMock(spec=use_cases.CheckConfigUseCase)

    api_router = fastapi.APIRouter()

    server = mock.MagicMock(spec=Server)
    server.get_api_router.return_value = api_router

    manager = Manager(
        generate_default_config_use_case=generate_default_config_use_case,
        check_config_use_case=check_config_use_case,
        server=server,
    )

    assert manager.get_server_api_router() == api_router
    server.get_api_router.assert_called()


def test_serve():
    generate_default_config_use_case = mock.MagicMock(spec=use_cases.GenerateDefaultConfigUseCase)

    check_config_use_case = mock.MagicMock(spec=use_cases.CheckConfigUseCase)
    check_config_use_case.execute.return_value = entities.ValidationReport()

    server = mock.MagicMock(spec=Server)

    manager = Manager(
        generate_default_config_use_case=generate_default_config_use_case,
        check_config_use_case=check_config_use_case,
        server=server,
    )

    manager.serve('0.0.0.0', port=9527)

    check_config_use_case.execute.assert_called_once()

    server.run.assert_called_with(
        host='0.0.0.0',
        port=9527,
    )
