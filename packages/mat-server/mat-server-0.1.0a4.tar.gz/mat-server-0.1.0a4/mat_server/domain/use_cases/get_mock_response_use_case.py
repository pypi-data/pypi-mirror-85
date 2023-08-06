import json

from mat_server.domain import base_types, entities, repositories, exceptions, helpers


class GetMockResponseUseCase(base_types.UseCase):

    def __init__(self,
                 mat_config_repository: repositories.MatConfigRepositoryBase,
                 file_helper: helpers.FileHelperBase):
        self._mat_config_repository = mat_config_repository
        self._file_helper = file_helper

    def execute(self, request: entities.ClientRequest) -> entities.ServerResponse:
        route_config = self._mat_config_repository.query_route_config(
            path=request.path,
            method=request.method,
            query_string=request.query_string,
        )

        if route_config is None:
            raise exceptions.NotFoundError('找不到對應的 ConfigRoute')

        if route_config.response.file_path and route_config.response.data:
            raise exceptions.ValidationError('回傳資源衝突')

        if route_config.response.data:
            file_type = self._guess_data_file(route_config.response)

            # 如果是 json
            if file_type == 'application/json':
                raw_body = json.dumps(route_config.response.data).encode()
            # 其餘直接編碼
            else:
                raw_body = route_config.response.data.encode()

            return entities.ServerResponse(
                raw_body=raw_body,
                status_code=route_config.status_code,
                headers={
                    'Content-Type': self._guess_data_file(route_config.response),
                },
            )

        elif route_config.response.file_path:
            response_file_path = self._file_helper.join_file_paths(
                'mat-data',
                route_config.response.file_path,
            )

            return entities.ServerResponse(
                raw_body=self._file_helper.read_bytes(response_file_path),
                status_code=route_config.status_code,
                headers={
                    'Content-Type': self._guess_data_file(route_config.response),
                },
            )

        else:
            raise exceptions.ValidationError('找不到對應的回傳資料')

    def _guess_data_file(self, response: entities.RouteResponseConfig):
        if response.data:
            # 如果是字串型態猜測為網頁
            if isinstance(response.data, str):
                return 'text/html; charset=utf-8'
            # 其餘猜測為 json
            else:
                return 'application/json'
        elif response.file_path:
            response_file_path = self._file_helper.join_file_paths(
                'mat-data',
                response.file_path,
            )

            file_type = self._file_helper.guess_file_type(response_file_path)
            # 如果猜不到就當作網頁
            if file_type is None:
                file_type = 'text/html; charset=utf-8'
            return file_type
        else:  # pragma: no cover
            raise exceptions.ValidationError('資訊不足，無法猜測資料型態')
