from unittest import mock

from mat_server.domain import repositories, entities
from mat_server.domain.use_cases.check_config_use_case import CheckConfigUseCase


def test_check_config_without_proxy_host_setting():
    mat_config_repository = mock.MagicMock(spec=repositories.MatConfigRepositoryBase)
    mat_config_repository.get_proxy_host.return_value = None

    uc = CheckConfigUseCase(
        mat_config_repository=mat_config_repository,
    )

    assert uc.execute() == entities.ValidationReport(
        failed_reasons=[
            '必須要有 proxy host 設定',
        ]
    )


def test_check_config_success():
    mat_config_repository = mock.MagicMock(spec=repositories.MatConfigRepositoryBase)
    mat_config_repository.get_proxy_host.return_value = "proxy_host"

    uc = CheckConfigUseCase(
        mat_config_repository=mat_config_repository,
    )

    assert uc.execute() == entities.ValidationReport()
