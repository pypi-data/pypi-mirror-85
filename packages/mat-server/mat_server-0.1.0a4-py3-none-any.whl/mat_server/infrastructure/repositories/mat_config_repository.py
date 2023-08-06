from typing import Optional

from mat_server.domain import repositories, entities, helpers


class MatConfigRepository(repositories.MatConfigRepositoryBase):
    CONFIG_DIR_PATH = './mat-data'
    CONFIG_FILE_PATH = './mat-data/config.yml'

    def __init__(self,
                 file_helper: helpers.FileHelperBase,
                 data_retriever_helper: helpers.DataRetrieverHelperBase):
        self._file_helper = file_helper
        self._data_retriever_helper = data_retriever_helper

    def get_config(self) -> entities.MatConfig:
        return entities.MatConfig(
            server=entities.ServerConfig(
                proxy_url=self.get_proxy_host(),
            ),
            routes=self.get_all_route_configs(),
        )

    def get_proxy_host(self) -> Optional[str]:
        data = self._file_helper.read_yaml(self.CONFIG_FILE_PATH)
        return self._data_retriever_helper.get_value(data, '.server.proxy_url')

    def query_route_config(self,
                           path: str,
                           method: str,
                           query_string: str) -> Optional[entities.RouteConfig]:
        route_configs = self.get_all_route_configs()
        for route_config in route_configs:
            if route_config.listen_path != path:
                continue

            if route_config.method != method:
                continue

            if not route_config.check_if_query_string_matches_config(query_string):
                continue

            return route_config
        return None

    def get_all_route_configs(self):
        data = self._file_helper.read_yaml(self.CONFIG_FILE_PATH)

        route_configs = []
        for route in self._data_retriever_helper.get_value(data, '.routes'):
            query = route.get('query')
            if query:
                for key, values in query.items():
                    if isinstance(values, str):
                        query[key] = [values]

            route_configs.append(entities.RouteConfig(
                listen_path=self._data_retriever_helper.get_value(route, '.listen_path'),
                method=self._data_retriever_helper.get_value(route, '.method', 'GET'),
                status_code=self._data_retriever_helper.get_value(route, '.status_code', 200),
                query=query,
                response=entities.RouteResponseConfig(
                    data=self._data_retriever_helper.get_value(route, '.response.data'),
                    file_path=self._data_retriever_helper.get_value(route, '.response.file_path'),
                )
            ))

        return route_configs
