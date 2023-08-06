from typing import Dict, Any

from mat_server.domain import base_types


class HTTPResponse(base_types.Entity):

    def __init__(self,
                 raw_data: bytes,
                 status_code: int,
                 headers: Dict[str, str]):
        self.raw_data = raw_data
        self.status_code = status_code
        self.headers = headers

    def __hash__(self):
        return hash((
            self.raw_data,
            self.status_code,
            frozenset(self.headers.items()),
        ))

    def __eq__(self, other: Any):
        if not isinstance(other, HTTPResponse):
            return False
        return hash(self) == hash(other)
