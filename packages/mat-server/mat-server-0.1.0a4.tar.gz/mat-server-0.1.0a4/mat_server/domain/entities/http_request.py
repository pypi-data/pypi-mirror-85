from typing import Dict, Any

from mat_server.domain import base_types


class HTTPRequest(base_types.Entity):

    def __init__(self,
                 url: str,
                 method: str = 'GET',
                 headers: Dict[str, str] = None,
                 raw_body: bytes = b''):
        self.url = url
        self.method = method
        self.headers = headers if headers is not None else {}
        self.raw_body = raw_body

    def __hash__(self):
        return hash((
            self.url,
            self.method,
            frozenset(self.headers.items()),
            self.raw_body,
        ))

    def __eq__(self, other: Any):
        if not isinstance(other, HTTPRequest):
            return False
        return hash(self) == hash(other)
