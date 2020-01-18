from flask import request


def get_request_info():
    if not bool(request):
        return None

    result = dict(
        method=request.method,
        url=request.url,
        headers=dict(request.headers),
        url_params=request.args,
        form_params=request.form,
        cookies=request.cookies
    )

    if request.data:
        result['payload'] = request.data.decode('utf-8')

    return result
