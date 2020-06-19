import falcon

from mest.webframeworks.base import WebFramework
from .inference_resource import InferenceResource


class Falcon(WebFramework):
    def __init__(self, predictor_cls):
        self.predictor_cls = predictor_cls
        self._app = falcon.API()

    def add_inference_route(self, rule, predictor):
        self._app.add_route(uri_template=rule,
                            resource=InferenceResource(self.predictor_cls))

    def add_get_route(self):
        pass

    @property
    def app(self):
        return self._app
