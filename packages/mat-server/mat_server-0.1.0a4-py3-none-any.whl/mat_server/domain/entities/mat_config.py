import urllib.parse
from typing import Dict, Optional, List, Any

from mat_server.domain import base_types


class RouteResponseConfig(base_types.Entity):
    def __init__(self,
                 file_path: Optional[str] = None,
                 data: Optional[Any] = None):
        self.file_path = file_path
        self.data = data

    def __eq__(self, other):
        if not isinstance(other, RouteResponseConfig):
            return False
        return self.serialize() == other.serialize()

    def serialize(self) -> dict:
        result = {}
        if self.file_path:
            result['file_path'] = self.file_path
        if self.data:
            result['data'] = self.data
        return result


class RouteConfig(base_types.Entity):
    def __init__(self,
                 listen_path: str,
                 method: str,
                 status_code: int,
                 query: Optional[Dict[str, List[str]]],
                 response: RouteResponseConfig):
        self.listen_path = listen_path
        self.method = method
        self.status_code = status_code
        self.query = query
        self.response = response

    def check_if_query_string_matches_config(self, query_string: str) -> bool:
        if self.query:
            query_params = urllib.parse.parse_qs(query_string)
            for key, values in self.query.items():
                if set(values) != set(query_params.get(key, [])):
                    return False
        return True

    def __eq__(self, other):
        if not isinstance(other, RouteConfig):
            return False
        return self.serialize() == other.serialize()

    def serialize(self) -> dict:
        return {
            'listen_path': self.listen_path,
            'method': self.method,
            'status_code': self.status_code,
            'query': self.query,
            'response': self.response.serialize(),
        }


class ServerConfig(base_types.Entity):
    def __init__(self, proxy_url: Optional[str]):
        self.proxy_url = proxy_url

    def serialize(self) -> dict:
        return {
            'proxy_url': self.proxy_url,
        }

    def __eq__(self, other):
        if not isinstance(other, ServerConfig):
            return False
        return self.serialize() == other.serialize()


class MatConfig(base_types.Entity):
    def __init__(self, server: ServerConfig, routes: List[RouteConfig]):
        self.server = server
        self.routes = routes

    def serialize(self) -> dict:
        return {
            'server': self.server.serialize(),
            'routes': [route.serialize() for route in self.routes],
        }

    def __eq__(self, other):
        if not isinstance(other, MatConfig):
            return False
        return self.serialize() == other.serialize()
