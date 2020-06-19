from abc import abstractmethod


class WebFramework:
    @abstractmethod
    def add_inference_route(self, rule, predictor):
        pass

    @abstractmethod
    def add_get_route(self):
        pass

    @abstractmethod
    @property
    def app(self):
        pass
