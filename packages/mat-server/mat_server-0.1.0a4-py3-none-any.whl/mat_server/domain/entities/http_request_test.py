from mat_server.domain.entities import HTTPRequest


def test_create_http_request_with_data():
    http_request = HTTPRequest(
        url='url',
        method='POST',
        headers={
            'Name': 'name',
        },
        raw_body=b'raw_body'
    )

    assert http_request.url == 'url'
    assert http_request.method == 'POST'
    assert http_request.headers == {
        'Name': 'name',
    }
    assert http_request.raw_body == b'raw_body'


def test_create_http_request_without_data():
    http_request = HTTPRequest(
        url='url',
    )

    assert http_request.url == 'url'
    assert http_request.method == 'GET'
    assert http_request.headers == {}
    assert http_request.raw_body == b''


def test_compare_different_type():
    assert HTTPRequest(
        url='url',
    ) != ''


def test_compare_different_url():
    assert HTTPRequest(
        url='url',
    ) != HTTPRequest(
        url='url2'
    )


def test_compare_different_method():
    assert HTTPRequest(
        url='url',
        method='GET',
    ) != HTTPRequest(
        url='url',
        method='POST',
    )


def test_compare_different_raw_body():
    assert HTTPRequest(
        url='url',
        raw_body=b'raw_body',
    ) != HTTPRequest(
        url='url',
        raw_body=b'raw_body2',
    )


def test_compare_different_headers():
    assert HTTPRequest(
        url='url',
        headers={
            'Name': 'name',
        },
    ) != HTTPRequest(
        url='url',
        headers={
            'Name': 'name2',
        },
    )


def test_compare_the_same_request():
    assert HTTPRequest(
        url='url',
    ) == HTTPRequest(
        url='url',
    )
