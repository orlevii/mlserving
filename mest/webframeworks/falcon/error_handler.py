from falcon import Request, Response, HTTPError
from mest.api import Response as MestResponse


def error_handler(handler):
    def falcon_handler(_: Request, resp: Response, ex, _params):
        r: MestResponse = handler(ex)

        if isinstance(ex, HTTPError):
            resp.status = ex.status
        else:
            resp.status = r.status_string
        resp.body = r.text

    return falcon_handler
