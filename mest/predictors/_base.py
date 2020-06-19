import abc


class PredictorBase:
    def __init__(self, model):
        self.model = model

    def predict(self, input_data):
        features = self.before_request(input_data)

        processed_data = self.pre_process(features)

        prediction = self.infer(processed_data)

        return self.post_process(prediction)

    def before_request(self, input_data):
        return input_data

    def pre_process(self, features):
        return features

    @abc.abstractmethod
    def infer(self, processed_data):
        pass

    def post_process(self, processed_data):
        return processed_data

