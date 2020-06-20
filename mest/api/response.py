import json
from http import HTTPStatus
from typing import Optional, Union


class Response:
    def __init__(self,
                 text: Optional[str] = None,
                 data: Optional[dict] = None,
                 status: Union[int, HTTPStatus] = HTTPStatus.OK,
                 content_type: str = 'application/json'):
        self._text = text
        self._data = data
        self.status = status
        self.content_type = content_type

    @property
    def data(self) -> Optional[dict]:
        if self._text is None and self._data is None:
            return None

        if self._data is None:
            self._data = json.loads(self._text)

        return self._data

    @property
    def text(self) -> Optional[str]:
        if self._text is None and self._data is None:
            return None

        if self._text is None:
            self._text = json.dumps(self._data)

        return self._text

    @property
    def status_string(self) -> str:
        s = self.status
        if isinstance(self.status, int):
            s = HTTPStatus(self.status)

        return f'{s.value} - {s.phrase}'
