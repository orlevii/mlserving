import abc


class GenericModel(object):
    def __init__(self):
        self.model = None

    @abc.abstractmethod
    def init(self, local_model_dir_path):
        pass

    def predict(self, **kwargs):
        inference_payload = self.pre_process(**kwargs)

        prediction = self.__invoke_with_expansion(method=self.infer,
                                                  payload=inference_payload)

        return self.__invoke_with_expansion(method=self.post_process,
                                            payload=prediction)

    def pre_process(self, **kwargs):
        return kwargs

    @abc.abstractmethod
    def infer(self, *args, **kwargs):
        pass

    def post_process(self, *args, **kwargs):
        if args:
            if len(args) == 1:
                return args[0]
            else:
                return args
        return kwargs

    def validate(self):
        pass

    @property
    def is_loaded(self):
        return self.model is not None

    @staticmethod
    def __invoke_with_expansion(method, payload):
        payload_type = type(payload)

        if payload_type == dict:
            return method(**payload)
        elif payload_type == list:
            return method(*payload)
        else:
            return method(payload)


class ModelValidationError(RuntimeError):
    pass
