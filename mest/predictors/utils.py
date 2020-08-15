from http import HTTPStatus

from mest.api import Response


def error_response(e: Exception):
    return Response(data={'error': str(e)},
                    status=HTTPStatus.INTERNAL_SERVER_ERROR)
