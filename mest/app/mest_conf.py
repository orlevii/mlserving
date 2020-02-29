import logging
import os


class Environment(object):
    TESTING = 'testing'
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'


class MestConfig(object):
    def __init__(self, service_name, listen_port, models_instances=[],
                 local_model_directory_path='_models'):
        self.service_name = service_name
        self.listen_port = listen_port
        self.models_instances = models_instances
        self.local_model_directory_path = local_model_directory_path

        self._setup_general()

    def _setup_general(self):
        self.env = os.environ.get('FLASK_ENV', Environment.DEVELOPMENT)
        self.debug = bool(os.environ.get('DEBUG', False))
        self.log_level = logging.ERROR
