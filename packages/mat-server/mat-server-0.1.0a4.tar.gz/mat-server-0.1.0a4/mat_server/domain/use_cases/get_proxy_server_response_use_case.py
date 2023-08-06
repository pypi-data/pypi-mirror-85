from mat_server.domain import base_types, entities, helpers, repositories

HOP_BY_HOP_HEADERS = frozenset(
    (
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "te",
        "trailers",
        "transfer-encoding",
        "upgrade",
    )
)


class GetProxyServerResponseUseCase(base_types.UseCase):

    def __init__(self,
                 mat_config_repository: repositories.MatConfigRepositoryBase,
                 request_helper: helpers.HTTPRequestHelperBase):
        self._mat_config_repository = mat_config_repository
        self._request_helper = request_helper

    def execute(self, request: entities.ClientRequest) -> entities.ServerResponse:
        # 取得 Proxy Server Url
        proxy_host = self._mat_config_repository.get_proxy_host()
        proxy_url = f'{proxy_host}/{request.path}?{request.query_string}'

        # 移除不必要的 Header
        headers = request.headers.copy()
        del headers['host']

        # 取得 Proxy Server 的回傳值
        http_response = self._request_helper.send(
            entities.HTTPRequest(
                method=request.method,
                url=proxy_url,
                headers=headers,
                raw_body=request.raw_body,
            )
        )

        # 將回傳值轉換為 mat Server 的回傳值
        headers = {
            name: value
            for name, value in http_response.headers.items() if name.lower() not in HOP_BY_HOP_HEADERS
        }

        return entities.ServerResponse(
            raw_body=http_response.raw_data,
            headers=headers,
            status_code=http_response.status_code,
        )
