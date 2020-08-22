import traceback
from http import HTTPStatus

from mlserving.api import Response


def error_response(e: Exception):
    data = {
        'error': str(e),
        'error_cls': type(e).__name__,
        'traceback': traceback.format_exc()
    }
    return Response(data=data,
                    status=HTTPStatus.INTERNAL_SERVER_ERROR)
