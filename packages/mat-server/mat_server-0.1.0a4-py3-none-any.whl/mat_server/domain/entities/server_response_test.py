from mat_server.domain.entities import ServerResponse


def test_create_server_response_without_data():
    server_response = ServerResponse()

    assert server_response.raw_body == b''
    assert server_response.status_code == 200
    assert server_response.headers == {}


def test_create_server_response_with_data():
    server_response = ServerResponse(
        raw_body=b'raw_body',
        status_code=201,
        headers={
            'Name': 'name'
        }
    )

    assert server_response.raw_body == b'raw_body'
    assert server_response.status_code == 201
    assert server_response.headers == {
        'Name': 'name'
    }


def test_compare_in_different_type():
    assert ServerResponse() != ''


def test_compare_in_different_raw_body_response():
    assert ServerResponse(
        raw_body=b'raw_body',
    ) != ServerResponse(
        raw_body=b'raw_body2',
    )


def test_compare_in_different_status_code_response():
    assert ServerResponse(
        status_code=200,
    ) != ServerResponse(
        status_code=201,
    )


def test_compare_in_different_headers_response():
    assert ServerResponse(
        headers={
            'Name': 'value',
        },
    ) != ServerResponse(
        headers={
            'Name': 'value2',
        }
    )


def test_compare_the_same_response():
    assert ServerResponse(
        raw_body=b'raw_body',
        status_code=200,
        headers={
            'Name': 'name'
        }
    ) == ServerResponse(
        raw_body=b'raw_body',
        status_code=200,
        headers={
            'Name': 'name'
        }
    )
