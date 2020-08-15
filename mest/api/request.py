from typing import Optional


class Request:
    def __init__(self,
                 payload: dict,
                 headers: Optional[dict] = None):
        self._payload = payload
        if headers is None:
            headers = {}
        self._headers = headers

    @property
    def payload(self):
        return self._payload

    @property
    def headers(self):
        return self._headers
