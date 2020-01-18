import json
from functools import wraps

from cerberus import Validator
from flask import request, current_app


def validate_params(schema):
    def decorator(func):
        @wraps(func)
        def wrapper():
            if request.method == 'GET':
                return __handle_get(schema, func)
            else:
                return __handle_other(schema, func)

        return wrapper

    return decorator


def __handle_get(schema, func):
    v = Validator()
    values = dict(request.values.items())
    if not v.validate(values, schema):
        current_app.logger.error({
            'msg': 'Error in validating request-params',
            'errors': v.errors
        })

        return json.dumps({'error': v.errors}), 400

    return func(**v.normalized(values))


def __handle_other(schema, func):
    v = Validator()
    try:
        if not request.is_json:
            error_message = 'Invalid "Content-Type", check your request-headers'
            current_app.logger.error(error_message)

            return json.dumps({'error': error_message}), 400
        else:
            params = dict(request.values.items(), **__get_json())
            if not v.validate(params, schema):
                current_app.logger.error({
                    'msg': 'Error in validating request-params',
                    'errors': v.errors
                })

                return json.dumps({'error': v.errors}), 400
    except Exception:
        error_message = 'Invalid JSON!'
        current_app.logger.error(error_message)

        return json.dumps({'error': error_message}), 400

    return func(**v.normalized(params))


def __get_json():
    if request.data == b"":
        return dict()

    return request.get_json()
