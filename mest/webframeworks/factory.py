class WebFrameworkFactory:

    @staticmethod
    def create(name: str):
        framework = FRAMEWORKS.get(name)
        if framework is None:
            raise NotImplementedError(f'Framework {name} is not implemented')

    @staticmethod
    def falcon():
        try:
            from .falcon import Falcon
        except ImportError:
            print('falcon >= 2 is required in order falcon as web-framework')


FRAMEWORKS = dict(
    falcon=WebFrameworkFactory.falcon
)
