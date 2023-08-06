from typing import Dict, Optional, Any

from mat_server.domain import base_types


class ClientRequest(base_types.Entity):
    """來自客戶端的 Request"""

    def __init__(self,
                 method: str = 'GET',
                 path: str = '',
                 query_string: str = '',
                 headers: Optional[Dict[str, str]] = None,
                 raw_body: bytes = b''):
        self.method = method

        self.path = path
        self.query_string = query_string

        if headers is None:
            headers = {}

        self.headers = {
            name.lower(): value
            for name, value in headers.items()
        }

        self.raw_body = raw_body

    def __hash__(self):
        return hash((
            self.method,
            self.path,
            self.query_string,
            frozenset(self.headers.items()),
            self.raw_body,
        ))

    def __eq__(self, other: Any):
        if not isinstance(other, ClientRequest):
            return False
        return hash(self) == hash(other)
