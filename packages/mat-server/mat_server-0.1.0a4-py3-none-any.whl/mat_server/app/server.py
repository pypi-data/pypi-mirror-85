from typing import Callable

import fastapi

from mat_server.domain import use_cases, entities


class Server:

    def __init__(self,
                 get_config_use_case: use_cases.GetConfigUseCase,
                 check_if_mock_response_exists_use_case: use_cases.CheckIfMockResponseExistsUseCase,
                 get_mock_response_use_case: use_cases.GetMockResponseUseCase,
                 get_proxy_server_response_use_case: use_cases.GetProxyServerResponseUseCase,
                 server_serve_func: Callable,
                 ):

        self._get_config_use_case = get_config_use_case
        self._check_if_mock_response_exists_use_case = check_if_mock_response_exists_use_case
        self._get_mock_response_use_case = get_mock_response_use_case
        self._get_proxy_server_response_use_case = get_proxy_server_response_use_case

        self._server_serve_func = server_serve_func

    def get_api_router(self):
        def transform_response_to_fastapi_response(response: entities.ServerResponse):
            return fastapi.Response(
                content=response.raw_body,
                headers=response.headers,
                status_code=response.status_code,
            )

        api_router = fastapi.APIRouter()

        @api_router.get('/_mat')
        async def get_config():
            mat_config = self._get_config_use_case.execute()
            return mat_config.serialize()

        @api_router.api_route('/{path:path}')
        async def proxy(path, request: fastapi.Request):
            client_request = entities.ClientRequest(
                method=request.method,
                path=path,
                query_string=str(request.query_params),
                headers=dict(request.headers),
                raw_body=await request.body()
            )

            # 檢查是否需要 mock response
            existed = self._check_if_mock_response_exists_use_case.execute(client_request)

            # 如果需要 mock
            if existed:
                mock_response = self._get_mock_response_use_case.execute(client_request)
                return transform_response_to_fastapi_response(mock_response)

            # 如果不需要 mock，直接轉給 proxy server
            else:
                proxy_server_response = self._get_proxy_server_response_use_case.execute(client_request)
                return transform_response_to_fastapi_response(proxy_server_response)

        return api_router

    def run(self, host: str, port: int):
        app = fastapi.FastAPI()
        app.include_router(self.get_api_router())
        self._server_serve_func(app, host=host, port=port)
