import os

from mest.models import GenericModel
from mest.app import MestConfig


class MyTestModel(GenericModel):
    def init(self, path):
        file_path = os.path.join(path, 'model.txt')
        with open(file_path, 'r') as fs:
            self.model = fs.read()

    def infer(self, *args, **kwargs):
        return self.model


def current_file_path():
    return os.path.dirname(os.path.abspath(__file__))


def generate_mest_config() -> MestConfig:
    return MestConfig(service_name='test_mest',
                      listen_port=1234)


def generate_mest_config_with_model() -> MestConfig:
    conf = generate_mest_config()
    conf.local_model_directory_path = os.path.join(current_file_path(), '_models')

    return conf
