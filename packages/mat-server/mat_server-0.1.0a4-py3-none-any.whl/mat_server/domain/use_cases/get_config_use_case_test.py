from unittest import mock

from mat_server.domain import repositories, entities
from mat_server.domain.use_cases import GetConfigUseCase


def test_get_mat_config():
    mat_config = entities.MatConfig(
        server=entities.ServerConfig(
            proxy_url='proxy_url',
        ),
        routes=[
            entities.RouteConfig(
                listen_path='listen_path',
                method='GET',
                status_code=200,
                query={
                    'key': ['value']
                },
                response=entities.RouteResponseConfig(
                    file_path='file_path',
                    data='data',
                )
            )
        ]
    )

    mat_config_repository = mock.MagicMock(spec=repositories.MatConfigRepositoryBase)
    mat_config_repository.get_config.return_value = mat_config

    uc = GetConfigUseCase(
        mat_config_repository=mat_config_repository,
    )

    assert uc.execute() == mat_config
