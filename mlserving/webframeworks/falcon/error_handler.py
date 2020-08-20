import falcon as f

from mlserving.api import Response


def error_handler(handler):
    def falcon_handler(_: f.Request, resp: f.Response, ex, _params):
        r: Response = handler(ex)

        if isinstance(ex, f.HTTPError):
            resp.status = ex.status
        else:
            resp.status = r.status_string
        resp.body = r.text

    return falcon_handler
