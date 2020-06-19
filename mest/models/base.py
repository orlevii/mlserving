from abc import abstractmethod

from mest.predictors import PredictorBase


class BaseModel:
    @abstractmethod
    def load(self, local_model_dir: str):
        """
        Loads all the relevant files needed in order to perform inference.

        @param local_model_dir: The local directory where all the files needed for this model are available.
        """
        pass

    @abstractmethod
    def create_predictor(self) -> PredictorBase:
        """
        @return: A new instance of your predictor
        This method will be called every inference.
        """
        pass
