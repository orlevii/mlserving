import os

from ganesha.models import GenericModel
from ganesha.app import JarvisConfiguration


class MyTestModel(GenericModel):
    def init(self, path):
        file_path = os.path.join(path, 'model.txt')
        with open(file_path, 'r') as fs:
            self.model = fs.read()

    def infer(self, *args, **kwargs):
        return self.model


def current_file_path():
    return os.path.dirname(os.path.abspath(__file__))


def generate_ganesha_config() -> JarvisConfiguration:
    return JarvisConfiguration(service_name='test_ganesha',
                               listen_port=1234)


def generate_ganesha_config_with_model() -> JarvisConfiguration:
    conf = generate_ganesha_config()
    conf.local_model_directory_path = os.path.join(current_file_path(), '_models')

    return conf
