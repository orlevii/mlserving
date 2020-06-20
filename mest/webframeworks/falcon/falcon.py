import falcon

from mest.webframeworks.base import WebFramework
from .error_handler import error_handler
from .health_resource import HealthResource
from .inference_resource import InferenceResource


class Falcon(WebFramework):

    def __init__(self):
        self._app = falcon.API()

    @property
    def app(self):
        return self._app

    def add_inference_handler(self, model, rule, **kwargs):
        self.app.add_route(uri_template=rule,
                           resource=InferenceResource(model))

    def add_health_handler(self, model, rule, **kwargs):
        self.app.add_route(uri_template=rule,
                           resource=HealthResource(model))

    def set_error_handler(self, handler):
        falcon_handler = error_handler(handler)

        self.app.add_error_handler(Exception, falcon_handler)