import json
import logging
import os
import signal
from typing import Union
from wsgiref import simple_server

from mest.app.api import Router
from .webframeworks import WebFramework, WebFrameworkFactory

os.environ.setdefault('MEST_APP', 'app.py')


class Mest(object):
    def __init__(self,
                 framework: Union[str, WebFramework] = 'falcon'):
        if isinstance(framework, WebFramework):
            self.web_framework = framework
        else:
            self.web_framework = WebFrameworkFactory.create(framework)

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

    def run(self, host='0.0.0.0', port=5000):

        if __name__ == '__main__':
            with simple_server.make_server(host, port, self.web_framework.app) as httpd:
                httpd.serve_forever()

    def register_router(self, url: str, router: Router):
        self.app.register_blueprint(router._blueprint, url_prefix=url)

    @property
    def logger(self):
        return self.app.logger

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
