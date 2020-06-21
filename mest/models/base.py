from abc import abstractmethod
from typing import NoReturn

from mest.app.health import HealthStatus, Healthy
from mest.predictors import BasePredictor


class BaseModel:
    """
    This class represents a loaded model
    __init__ should loads all the relevant data needed in order to perform inference.
    """

    @abstractmethod
    def create_predictor(self) -> BasePredictor:
        """
        @return: A new instance of your predictor
        This method will be called every inference.
        """
        pass

    def health_status(self) -> HealthStatus:
        """
        @return: Given the state of this model-instance, can the inference be performed?
        This method is used for health-checks.
        It's not recommended to run here complex computation.
        """
        return Healthy()
