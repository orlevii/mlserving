import logging

try:
    import requests
except ImportError as e:
    logger = logging.getLogger('mlserving')
    logger.exception('Using TFServingPrediction requires requests to be installed')


class TFServingRequestError(Exception):
    pass


class TFServingPrediction:
    def __init__(self, host='127.0.0.1', port=8501, model_name='model',
                 predict_api_url=None, **kwargs):
        """
        :param host: The tf-serving server host address
        :param port: REST-api port
        :param model_name: The name of the model to invoke
        :param predict_api_url: Full url for invocation
        :param kwargs: optional arguments for `requests.post` method

        To initialize it properly, you have to specify [host, port, model_name]
        OR [predict_api_url]

        if predict_api_url is sent, it will be prioritized
        """
        if predict_api_url:
            self.predict_api_url = predict_api_url
        else:
            self.predict_api_url = f'http://{host}:{port}/v1/models/{model_name}:predict'

        self._requests_options = kwargs

    def predict(self, request_payload: dict, req):
        res = requests.post(self.predict_api_url, json=request_payload, **self._requests_options)
        if res.status_code != 200:
            raise TFServingRequestError(f'Failed calling tf-serving endpoint, code: {res.status_code}, {res.content}')

        return res.json()
