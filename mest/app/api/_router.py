import datetime
import json

from flask import Blueprint, current_app

from ._request_parser import validate_params
from .health.health_check import generate_models_health_check
from .health.health_runner import HealthRunner


class Router(object):
    def __init__(self, name):
        self._blueprint = Blueprint(name, __name__)

    def route(self, url, method='POST', **options):
        def decorator(func):
            methods = options.pop('methods', [method])

            blueprint_decorator = self._blueprint.route(url, methods=methods, endpoint=func.__name__, **options)

            return blueprint_decorator(func)

        return decorator

    def add_predict_route(self, model_instance, schema, url='/predict', method='POST'):
        @self.route(url, method=method)
        @validate_params(schema=schema)
        def predict(**params):
            try:
                result = model_instance.predict(**params)

                return json.dumps(result)
            except Exception as e:
                response = {'message': str(e)}

                return json.dumps(response), 500

    def add_ping_route(self, url='/ping', method='GET'):
        @self.route(url=url, method=method)
        def ping():
            msg = 'Pong from {}! - {}'.format(current_app.config['MEST'].service_name,
                                              datetime.datetime.now())

            return json.dumps({'message': msg})

    def add_health_check_route(self, model_health_methods=None, url='/health', method='GET'):
        if model_health_methods is None:
            model_health_methods = generate_models_health_check()

        @self.route(url=url, method=method)
        def health():
            HealthRunner.run(model_health_methods)
