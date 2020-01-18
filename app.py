import logging

from jarvis.app import Jarvis, JarvisConfiguration
from jarvis.app.api import generate_api_v1
from jarvis.cli import jarvis_cli
from jarvis.models import GenericModel


class MyTestModel(GenericModel):
    def init(self, path):
        self.model = 'hello'


def register_cli_commands():
    @jarvis_cli.command(name='hello', help='Prints hello world to the console')
    def hello():
        print('hello world!')


def register_routes(jarvis_app):
    api_v1 = generate_api_v1()

    jarvis_app.register_router(url='/api/v1',
                               router=api_v1)


model = MyTestModel()

conf = JarvisConfiguration(service_name='test_jarvis',
                           listen_port=1234,
                           models_instances=[model])

jarvis_app = Jarvis(conf).setup()

register_routes(jarvis_app)

# register_cli_commands()

logger = logging.getLogger('test_jarvis')
# logger.debug('Works!')

if __name__ == '__main__':
    jarvis_app.run()
