import logging
import signal
import sys
from http import HTTPStatus
from typing import Union
from wsgiref import simple_server

from .api import Response
from .app.state import runtime_state
from .webframeworks import WebFramework, WebFrameworkFactory


class Mest(object):
    def __init__(self,
                 framework: Union[str, WebFramework] = 'falcon',
                 **kwargs):
        """
        Initialized mest-application
        @param framework: The web-framework to use
            (default: "falcon")
        @param kwargs: Additional configs, currently not in use.
        """
        if isinstance(framework, WebFramework):
            self.web_framework = framework
        else:
            self.web_framework = WebFrameworkFactory.create(framework)

        self.__init_logger()
        self._handle_sigterm(self.logger)

        err_handler = self.get_default_error_handler()
        self.web_framework.set_error_handler(err_handler)

    def add_inference_handler(self, model, rule, **kwargs):
        self.web_framework.add_inference_handler(model, rule, **kwargs)

    def add_health_handler(self, model, rule, **kwargs):
        self.web_framework.add_health_handler(model, rule, **kwargs)

    def run(self, host='0.0.0.0', port=5000):
        with simple_server.make_server(host, port, self.app) as httpd:
            self.logger.info('Running development server on: http://{}:{}/'.format(host, port))
            self.logger.warning('NOTICE! Running development server on production environment is not recommended.')
            httpd.serve_forever()

    @property
    def logger(self):
        return logging.getLogger('mest')

    @staticmethod
    def __init_logger():
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
        stdout_handler.setFormatter(formatter)

        logger = logging.getLogger('mest')
        logger.setLevel(logging.INFO)
        logger.addHandler(stdout_handler)
        return logger

    @property
    def app(self):
        return self.web_framework.app

    @staticmethod
    def _handle_sigterm(logger):
        def sigterm_handler(_signum, _frame):
            logger.info('SIGTERM ACCEPTED')
            runtime_state.set_to_shutting_down()

        signal.signal(signal.SIGTERM, sigterm_handler)

    def get_default_error_handler(self):
        def handler(e: Exception) -> Response:
            self.logger.exception(e)
            return Response(data={'message': '{} {}'.format(type(e).__name__, e).strip()},
                            status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return handler
