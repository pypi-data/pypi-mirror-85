from typing import Optional, Dict, Any

from mat_server.domain import base_types


class ServerResponse(base_types.Entity):
    """傳給客戶端的回傳值"""

    def __init__(self,
                 raw_body: bytes = b'',
                 status_code: int = 200,
                 headers: Optional[Dict[str, str]] = None):
        self.raw_body = raw_body
        self.status_code = status_code
        self.headers = headers if headers is not None else {}

    def __eq__(self, other: Any):
        if not isinstance(other, ServerResponse):
            return False
        if self.raw_body != other.raw_body:
            return False
        if self.status_code != other.status_code:
            return False
        if self.headers != other.headers:
            return False
        return True
