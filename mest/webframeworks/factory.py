from mest.webframeworks import WebFramework


class WebFrameworkFactory:

    @staticmethod
    def create(name: str) -> WebFramework:
        framework = FRAMEWORKS.get(name)
        if framework is None:
            raise NotImplementedError(f'Framework {name} is not implemented')

        return framework()

    @staticmethod
    def _falcon():
        try:
            from .falcon import Falcon
        except ImportError:
            print('falcon >= 2 is required in order falcon as web-framework')


FRAMEWORKS = dict(
    falcon=WebFrameworkFactory._falcon
)
