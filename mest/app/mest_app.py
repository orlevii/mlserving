import json
import logging
import os
import signal

from flask import Flask

from ._logs.initializers import get_stdout_handler
from ._middlewares.response_time import RequestStatter
from ._state import runtime_state
from .api import Router
from .mest_conf import MestConfig, Environment

os.environ.setdefault('MEST_APP', 'app.py')


class Mest(object):
    def __init__(self, config: MestConfig):
        self.config = config
        self.app: Flask = self.__create_flask_app()
        self.__init_logger()
        self._setup = False

    def setup(self):
        if self.__is_cli:
            self._expose_app_for_gunicorn()
            return self
        if self._setup:
            return self

        _handle_sigterm(self.logger)
        _register_error_handler(self.app)

        self.load_models()

        self._setup = True

        return self

    def run(self):
        if not self._setup:
            raise RuntimeError('setup() must be called before run()')

        self.app.run(port=self.config.listen_port,
                     host='0.0.0.0')

    def register_router(self, url: str, router: Router):
        self.app.register_blueprint(router._blueprint, url_prefix=url)

    @property
    def logger(self):
        return self.app.logger

    def __create_flask_app(self) -> Flask:
        app = Flask(__name__)
        app.config['MEST'] = self.config

        # stats middleware
        RequestStatter(app, service_name=self.config.service_name)

        # logger
        if not self.config.debug:
            app.logger.handlers = []

        stdout_handler = get_stdout_handler(self.config.service_name)
        if self.config.env == Environment.DEVELOPMENT:
            stdout_handler.setLevel(logging.DEBUG)

        if not self.config.debug:
            app.logger.addHandler(stdout_handler)

        app.logger.setLevel(logging.DEBUG)

        return app

    def load_models(self):
        model_instance_name = None
        try:
            for model_instance in self.config.models_instances:
                model_instance_name = type(model_instance).__name__
                model_instance.init(self.config.local_model_directory_path)
                self.logger.debug('Initialized model {} successfully'.format(model_instance_name))
        except Exception:
            self.app.logger.exception('Could not initialize model: {}'.format(model_instance_name))
            if self.config.env == Environment.PRODUCTION:
                raise

    @property
    def __is_cli(self) -> bool:
        cli = os.environ.get('MEST_CLI', '')

        return cli.lower() == 'true'

    def __init_logger(self):
        logger = logging.getLogger(self.config.service_name)
        logger.setLevel(self.logger.level)
        logger.handlers = self.logger.handlers

    def _expose_app_for_gunicorn(self):
        main_app_module = os.environ.get('MEST_APP').split('.')[0]
        main_module = __import__(main_app_module)
        main_module.app = self.app


def _handle_sigterm(logger):
    def sigterm_handler(signum, frame):
        logger.info('SIGTERM ACCEPTED')
        runtime_state.set_to_shutting_down()

    signal.signal(signal.SIGTERM, sigterm_handler)


def _register_error_handler(app):
    @app.errorhandler(Exception)
    def generic_exception_handler(error):
        app.logger.exception(error)

        return json.dumps({'message': str(error)}), 500

    @app.errorhandler(404)
    def not_found(error):
        app.logger.info(error)

        return json.dumps({'message': '{}'.format(error)}), 404
