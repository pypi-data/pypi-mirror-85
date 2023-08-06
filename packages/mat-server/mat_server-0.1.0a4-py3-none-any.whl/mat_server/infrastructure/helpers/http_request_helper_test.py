from unittest import mock

from mat_server.domain import entities
from mat_server.infrastructure.helpers import HTTPRequestHelper


def test_send():
    http_request = entities.HTTPRequest(
        url='url',
        headers={
            'key': 'value',
        },
        raw_body=b'raw_body',
    )

    request = mock.MagicMock()

    response = mock.MagicMock()
    response.raw.read.return_value = b'data'
    response.status_code = 200
    response.headers = {
        'Key': 'Value'
    }

    session = mock.MagicMock()
    session.send.return_value = response

    requests_module = mock.MagicMock()
    requests_module.Session.return_value = session
    requests_module.Request.return_value = request

    http_request_helper = HTTPRequestHelper(
        requests_module=requests_module,
    )

    assert http_request_helper.send(http_request) == entities.HTTPResponse(
        raw_data=response.raw.read.return_value,
        status_code=response.status_code,
        headers={
            'key': 'Value',
        }
    )

    requests_module.Request.assert_called_with(
        method=http_request.method,
        url=http_request.url,
        headers=http_request.headers,
        data=http_request.raw_body,
    )

    session.send.assert_called_with(request.prepare.return_value, stream=True)
