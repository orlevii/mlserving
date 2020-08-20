from http import HTTPStatus

from mlserving.api import Response


def error_response(e: Exception):
    return Response(data={'error': str(e)},
                    status=HTTPStatus.INTERNAL_SERVER_ERROR)
