from mat_server.domain.entities import RouteResponseConfig, RouteConfig, ServerConfig, MatConfig


def test_create_route_response_config_with_data():
    route_response_config = RouteResponseConfig(
        file_path='file_path',
        data='data'
    )

    assert route_response_config.file_path == 'file_path'
    assert route_response_config.data == 'data'


def test_create_route_response_config_without_data():
    route_response_config = RouteResponseConfig()

    assert route_response_config.file_path is None
    assert route_response_config.data is None


def test_compare_route_response_config_in_different_type():
    assert RouteResponseConfig() != ''


def test_compare_route_response_config_in_different_file_path():
    assert RouteResponseConfig(
        file_path='file_path',
    ) != RouteResponseConfig(
        file_path='file_path2',
    )


def test_compare_route_response_config_in_different_data():
    assert RouteResponseConfig(
        data='data',
    ) != RouteResponseConfig(
        data='data2',
    )


def test_create_route_config_with_data():
    route_config = RouteConfig(
        listen_path='listen_path',
        method='GET',
        status_code=200,
        query={
            'name': ['Marco']
        },
        response=RouteResponseConfig(),
    )

    assert route_config.listen_path == 'listen_path'
    assert route_config.method == 'GET'
    assert route_config.status_code == 200
    assert route_config.query == {
        'name': ['Marco']
    }
    assert route_config.response == RouteResponseConfig()


def test_compare_route_config_in_different_type():
    assert RouteConfig(
        listen_path='listen_path',
        method='GET',
        status_code=200,
        query={
            'name': ['Marco']
        },
        response=RouteResponseConfig(),
    ) != ''


def test_compare_route_config_in_different_listen_path():
    assert RouteConfig(
        listen_path='listen_path',
        method='GET',
        status_code=200,
        query={
            'name': ['Marco']
        },
        response=RouteResponseConfig(),
    ) != RouteConfig(
        listen_path='listen_path2',
        method='GET',
        status_code=200,
        query={
            'name': ['Marco']
        },
        response=RouteResponseConfig(),
    )


def test_compare_route_config_in_different_method():
    assert RouteConfig(
        listen_path='listen_path',
        method='GET',
        status_code=200,
        query={
            'name': ['Marco']
        },
        response=RouteResponseConfig(),
    ) != RouteConfig(
        listen_path='listen_path',
        method='POST',
        status_code=200,
        query={
            'name': ['Marco']
        },
        response=RouteResponseConfig(),
    )


def test_compare_route_config_in_different_status_code():
    assert RouteConfig(
        listen_path='listen_path',
        method='GET',
        status_code=200,
        query={
            'name': ['Marco']
        },
        response=RouteResponseConfig(),
    ) != RouteConfig(
        listen_path='listen_path',
        method='GET',
        status_code=201,
        query={
            'name': ['Marco']
        },
        response=RouteResponseConfig(),
    )


def test_compare_route_config_in_different_query():
    assert RouteConfig(
        listen_path='listen_path',
        method='GET',
        status_code=200,
        query={
            'name': ['Marco']
        },
        response=RouteResponseConfig(),
    ) != RouteConfig(
        listen_path='listen_path',
        method='GET',
        status_code=201,
        query={
            'name': ['Marco2']
        },
        response=RouteResponseConfig(),
    )


def test_compare_route_config_in_different_response():
    assert RouteConfig(
        listen_path='listen_path',
        method='GET',
        status_code=200,
        query={
            'name': ['Marco']
        },
        response=RouteResponseConfig(),
    ) != RouteConfig(
        listen_path='listen_path',
        method='GET',
        status_code=201,
        query={
            'name': ['Marco']
        },
        response=RouteResponseConfig(
            file_path='file_path'
        ),
    )


def test_create_server_config():
    server_config = ServerConfig(
        proxy_url='proxy_url'
    )

    assert server_config.proxy_url == 'proxy_url'


def test_compare_server_config_in_different_type():
    assert ServerConfig(
        proxy_url='proxy_url'
    ) != ''


def test_compare_server_config_in_different_proxy_url():
    assert ServerConfig(
        proxy_url='proxy_url'
    ) != ServerConfig(
        proxy_url='proxy_url2'
    )


def test_create_mat_config():
    server_config = ServerConfig(
        proxy_url='proxy_url',
    )

    route_configs = [
        RouteConfig(
            listen_path='listen_path',
            method='GET',
            status_code=200,
            query={
                'key': ['value']
            },
            response=RouteResponseConfig(
                file_path='file_path',
                data='data',
            )
        )
    ]

    mat_config = MatConfig(
        server=server_config,
        routes=route_configs
    )

    assert mat_config.server == server_config
    assert mat_config.routes == route_configs


def test_compare_mat_config_in_different_type():
    assert MatConfig(
        server=ServerConfig(
            proxy_url='proxy_url',
        ),
        routes=[
            RouteConfig(
                listen_path='listen_path',
                method='GET',
                status_code=200,
                query={
                    'key': ['value']
                },
                response=RouteResponseConfig(
                    file_path='file_path',
                    data='data',
                )
            )
        ],
    ) != ''


def test_compare_mat_config_in_different_server():
    assert MatConfig(
        server=ServerConfig(
            proxy_url='proxy_url',
        ),
        routes=[
            RouteConfig(
                listen_path='listen_path',
                method='GET',
                status_code=200,
                query={
                    'key': ['value']
                },
                response=RouteResponseConfig(
                    file_path='file_path',
                    data='data',
                )
            )
        ],
    ) != MatConfig(
        server=ServerConfig(
            proxy_url='proxy_url2',
        ),
        routes=[
            RouteConfig(
                listen_path='listen_path',
                method='GET',
                status_code=200,
                query={
                    'key': ['value']
                },
                response=RouteResponseConfig(
                    file_path='file_path',
                    data='data',
                )
            )
        ],
    )


def test_compare_mat_config_in_different_routes():
    assert MatConfig(
        server=ServerConfig(
            proxy_url='proxy_url',
        ),
        routes=[
            RouteConfig(
                listen_path='listen_path',
                method='GET',
                status_code=200,
                query={
                    'key': ['value']
                },
                response=RouteResponseConfig(
                    file_path='file_path',
                    data='data',
                )
            )
        ],
    ) != MatConfig(
        server=ServerConfig(
            proxy_url='proxy_url',
        ),
        routes=[
            RouteConfig(
                listen_path='listen_path2',
                method='GET',
                status_code=200,
                query={
                    'key': ['value']
                },
                response=RouteResponseConfig(
                    file_path='file_path',
                    data='data',
                )
            )
        ],
    )
