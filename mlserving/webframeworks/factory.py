from mlserving.webframeworks import WebFramework


class WebFrameworkFactory:

    @staticmethod
    def create(name: str) -> WebFramework:
        framework_creator = FRAMEWORKS.get(name)
        if framework_creator is None:
            raise NotImplementedError(f'Framework {name} is not implemented')

        return framework_creator()

    @staticmethod
    def _create_falcon():
        try:
            from .falcon import FalconFramework
            return FalconFramework()
        except ImportError:
            print('falcon >= 2 is required in order falcon as web-framework')


FRAMEWORKS = dict(
    falcon=WebFrameworkFactory._create_falcon
)
