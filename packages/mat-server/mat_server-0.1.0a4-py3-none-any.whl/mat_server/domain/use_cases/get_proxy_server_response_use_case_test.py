from unittest import mock

from mat_server.domain import entities, helpers, repositories
from mat_server.domain.use_cases import GetProxyServerResponseUseCase


def test_get_proxy_server_response():
    mat_config_repository = mock.MagicMock(spec=repositories.MatConfigRepositoryBase)
    mat_config_repository.get_proxy_host.return_value = 'https://paji.marco79423.net'

    request_helper = mock.MagicMock(spec=helpers.HTTPRequestHelperBase)
    request_helper.send.return_value = entities.HTTPResponse(
        raw_data=b'raw_data',
        status_code=200,
        headers={
            'Name': 'name',
            'connection': 'Close',
        },
    )

    uc = GetProxyServerResponseUseCase(
        mat_config_repository=mat_config_repository,
        request_helper=request_helper,
    )

    server_response = uc.execute(
        request=entities.ClientRequest(
            method='GET',
            path='path',
            query_string='name=name',
            headers={
                'Host': 'host',
                'Name': 'name',
            }
        )
    )

    assert server_response == entities.ServerResponse(
        raw_body=b'raw_data',
        status_code=200,
        headers={
            'Name': 'name',
        },
    )

    request_helper.send.assert_called_with(entities.HTTPRequest(
        url='https://paji.marco79423.net/path?name=name',
        method='GET',
        headers={
            'name': 'name',
        },
        raw_body=b'',
    ))
