import abc


class HealthStatus:
    def __init__(self, message: str = None):
        self.message = message

    @property
    @abc.abstractmethod
    def healthy(self) -> bool:
        raise NotImplementedError()


class Healthy(HealthStatus):
    def __init__(self):
        super().__init__()

    @property
    def healthy(self) -> bool:
        return True


class Unhealthy(HealthStatus):
    def __init__(self, message: str = None):
        super().__init__(message)

    @property
    def healthy(self) -> bool:
        return False
