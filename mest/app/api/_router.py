from flask import Blueprint
from ._request_parser import validate_params
import json


class Router(object):
    def __init__(self, name):
        self._blueprint = Blueprint(name, __name__)

    def route(self, url, method='POST', **options):
        def decorator(func):
            methods = options.pop('methods', [method])

            blueprint_decorator = self._blueprint.route(url, methods=methods, endpoint=func.__name__, **options)

            return blueprint_decorator(func)

        return decorator

    def simple_predict(self, model_instance, schema, url='/predict', method='POST'):
        @self.route(url, method=method)
        @validate_params(schema=schema)
        def predict(**params):
            try:
                result = model_instance.predict(**params)

                return json.dumps(result)
            except Exception as e:
                response = {'message': str(e)}

                return json.dumps(response), 500
