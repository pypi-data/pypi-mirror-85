from mat_server.domain.entities import ClientRequest


def test_create_client_request_with_data():
    client_request = ClientRequest(
        method='POST',
        path='path',
        query_string='name=name',
        headers={
            'Name': 'name',
        },
        raw_body=b'hello world'
    )

    assert client_request.method == 'POST'
    assert client_request.path == 'path'
    assert client_request.query_string == 'name=name'
    assert client_request.headers == {
        'name': 'name'
    }
    assert client_request.raw_body == b'hello world'


def test_create_client_request_without_data():
    client_request = ClientRequest()

    assert client_request.method == 'GET'
    assert client_request.path == ''
    assert client_request.query_string == ''
    assert client_request.headers == {}
    assert client_request.raw_body == b''


def test_compare_in_different_type():
    assert ClientRequest() != ''


def test_compare_in_different_method():
    assert ClientRequest(
        method='GET',
    ) != ClientRequest(
        method='POST',
    )


def test_compare_in_different_path():
    assert ClientRequest(
        path='path',
    ) != ClientRequest(
        path='path2',
    )


def test_compare_in_different_query_string():
    assert ClientRequest(
        query_string='query_string',
    ) != ClientRequest(
        query_string='query_string2',
    )


def test_compare_in_different_headers():
    assert ClientRequest(
        headers={
            'name': 'name'
        },
    ) != ClientRequest(
        headers={
            'name': 'name2'
        },
    )


def test_compare_in_different_raw_body():
    assert ClientRequest(
        raw_body=b'raw_body',
    ) != ClientRequest(
        raw_body=b'raw_body2',
    )
