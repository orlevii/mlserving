import falcon

from mest.webframeworks.base import BaseWebFramework
from .inference_resource import InferenceResource


class Falcon(BaseWebFramework):
    def __init__(self, predictor_cls):
        self.predictor_cls = predictor_cls
        self.app = falcon.API()

    def add_inference_route(self, rule, predictor):
        self.app.add_route(uri_template=rule,
                           resource=InferenceResource(self.predictor_cls))

    def add_get_route(self):
        pass
