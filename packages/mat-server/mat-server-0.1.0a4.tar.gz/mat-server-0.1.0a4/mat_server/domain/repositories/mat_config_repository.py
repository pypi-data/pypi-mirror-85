import abc
from typing import Optional

from mat_server.domain import base_types, entities


class MatConfigRepositoryBase(base_types.Repository):

    @abc.abstractmethod
    def get_config(self) -> entities.MatConfig:
        pass

    @abc.abstractmethod
    def get_proxy_host(self) -> Optional[str]:
        pass

    @abc.abstractmethod
    def query_route_config(self,
                           path: str,
                           method: str,
                           query_string: str) -> Optional[entities.RouteConfig]:
        pass
