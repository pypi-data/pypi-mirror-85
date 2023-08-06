from mat_server.domain.entities import HTTPResponse


def test_create_http_response():
    http_response = HTTPResponse(
        raw_data=b'raw_data',
        status_code=200,
        headers={
            'name': 'name',
        }
    )

    assert http_response.raw_data == b'raw_data'
    assert http_response.status_code == 200
    assert http_response.headers == {
        'name': 'name',
    }


def test_compare_different_type():
    assert HTTPResponse(
        raw_data=b'raw_data',
        status_code=200,
        headers={
            'name': 'name',
        }
    ) != ''


def test_compare_different_raw_data():
    assert HTTPResponse(
        raw_data=b'raw_data',
        status_code=200,
        headers={
            'name': 'name',
        }
    ) != HTTPResponse(
        raw_data=b'raw_data2',
        status_code=200,
        headers={
            'name': 'name',
        }
    )


def test_compare_different_status_code():
    assert HTTPResponse(
        raw_data=b'raw_data',
        status_code=200,
        headers={
            'name': 'name',
        }
    ) != HTTPResponse(
        raw_data=b'raw_data',
        status_code=400,
        headers={
            'name': 'name',
        }
    )


def test_compare_different_headers():
    assert HTTPResponse(
        raw_data=b'raw_data',
        status_code=200,
        headers={
            'name': 'name',
        }
    ) != HTTPResponse(
        raw_data=b'raw_data',
        status_code=200,
        headers={
            'name': 'name2',
        }
    )
