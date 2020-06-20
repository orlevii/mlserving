from abc import abstractmethod


class WebFramework:
    @abstractmethod
    def add_inference_route(self, rule, model):
        pass

    @abstractmethod
    def add_health_route(self, rule, model):
        pass

    @property
    @abstractmethod
    def app(self):
        pass

    @abstractmethod
    def set_error_handler(self, handler):
        pass
