from abc import abstractmethod

from mest.predictors import PredictorBase
from typing import NoReturn


class BaseModel:
    @abstractmethod
    def load(self) -> NoReturn:
        """
        Loads all the relevant files needed in order to perform inference.
        """
        pass

    @abstractmethod
    def create_predictor(self) -> PredictorBase:
        """
        @return: A new instance of your predictor
        This method will be called every inference.
        """
        pass

    @property
    def is_healthy(self) -> bool:
        return True
