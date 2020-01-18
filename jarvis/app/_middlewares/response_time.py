import time
from multiprocessing.dummy import Pool as ThreadPool

from flask import g, request


class RequestStatter(object):
    def __init__(self, app=None, service_name='py_model', config=None, report_method=None):
        self.config = config
        self.prefix = 'services.{}'.format(service_name)
        self.pool = ThreadPool(1)
        self.report_method = report_method

        self.blacklist_routes = {u'get:/api/v1/ping', u'get:/api/v1/health'}

        # If an app was provided, then call `init_app` for them
        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app, config=None):

        # Used passed in config if provided, otherwise use the config from `app`
        if config is not None:
            self.config = config
        elif self.config is None:
            self.config = app.config

        self.app = app

        # Configure any of our middleware
        self.setup_middleware()

    def setup_middleware(self):
        """Helper to configure/setup any Flask-Datadog middleware"""
        # Configure response time middleware (if desired)
        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)

    def before_request(self):
        """
        middleware handle for before each request
        """
        # Set the request start time
        g.flask_request_start_time = time.time()

    def after_request(self, response):
        """
        middleware handler for after each request
        :param response: the response to be sent to the client
        :type response: ``flask.Response``
        :rtype: ``flask.Response``
        """
        # Return early if we don't have the start time
        if not hasattr(g, 'flask_request_start_time'):
            return response

        if request.url_rule is None:
            return response

        # Get the response time for this request
        elapsed = time.time() - g.flask_request_start_time
        # Convert the elapsed time to milliseconds if they want them
        elapsed = int(round(1000 * elapsed))

        request_method = request.method
        request_path = request.path
        response_status_code = response.status_code

        # encapsulate the vars above, and make a method for reporting stats
        def apply_report():
            try:
                blacklisted = self._is_blacklisted(request_method, request_path)
                if not blacklisted:
                    self.app.logger.debug(
                        "[{}] {} [{}] Time: {}ms".format(request_method, request_path, response_status_code, elapsed))

                    if self.report_method:
                        self.report_method(request_method=request_method, request_path=request_path,
                                           response_status_code=response_status_code, elapsed=elapsed)

            except Exception as e:
                self.app.logger.debug(e, exc_info=True)

        # spawn an async task for reporting our metrics
        self.pool.apply_async(apply_report)

        # We ALWAYS have to return the original response
        return response

    def _is_blacklisted(self, method, url_path):
        return "{}:{}".format(method.lower(), url_path.lower()) in self.blacklist_routes
