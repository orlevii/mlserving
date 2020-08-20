from abc import abstractmethod

from .status import HealthStatus, Healthy


class HealthHandler:
    @abstractmethod
    def health_check(self) -> HealthStatus:
        """
        @return: HealthStatus of your application / models / etc...
        """
        pass


class DefaultHealthHandler(HealthHandler):
    def health_check(self) -> HealthStatus:
        return Healthy()
