from abc import abstractmethod


class WebFramework:
    @abstractmethod
    def add_inference_handler(self, rule, predictor, **kwargs):
        pass

    @abstractmethod
    def add_health_handler(self, rule, health_handler, **kwargs):
        pass

    @property
    @abstractmethod
    def app(self):
        pass

    @abstractmethod
    def set_error_handler(self, handler):
        pass
