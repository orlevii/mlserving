import logging
import signal
import sys
from http import HTTPStatus
from typing import Union
from wsgiref import simple_server

from .api import Response
from mlserving.health import DefaultHealthHandler
from mlserving._state import runtime_state
from .webframeworks import WebFramework, WebFrameworkFactory

default_health_handler = DefaultHealthHandler()


class ServingApp(object):
    def __init__(self,
                 framework: Union[str, WebFramework] = 'falcon',
                 **kwargs):
        """
        Initialized mlserving-application
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

    def add_inference_handler(self, rule, predictor, **kwargs):
        self.web_framework.add_inference_handler(rule, predictor, **kwargs)

    def add_health_handler(self, rule, health_handler=default_health_handler, **kwargs):
        self.web_framework.add_health_handler(rule, health_handler, **kwargs)

    def run(self, host='0.0.0.0', port=5000):
        with simple_server.make_server(host, port, self) as httpd:
            self.logger.info(f'Running development server on: http://{host}:{port}/')
            self.logger.warning('NOTICE! Running development server on production environment is not recommended.')
            httpd.serve_forever()

    @property
    def logger(self):
        return logging.getLogger('mlserving')

    @staticmethod
    def __init_logger():
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
        stdout_handler.setFormatter(formatter)

        logger = logging.getLogger('mlserving')
        logger.setLevel(logging.INFO)
        logger.addHandler(stdout_handler)
        return logger

    def __call__(self, env, start_response):
        """
        For WSGI application
        """
        return self.web_framework.app(env, start_response)

    @staticmethod
    def _handle_sigterm(logger):
        def sigterm_handler(_signum, _frame):
            logger.info('SIGTERM ACCEPTED')
            runtime_state.set_to_shutting_down()

        signal.signal(signal.SIGTERM, sigterm_handler)

    def get_default_error_handler(self):
        def handler(e: Exception) -> Response:
            self.logger.exception(e)
            return Response(data={'message': f'{type(e).__name__} {e}'.strip()},
                            status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return handler
