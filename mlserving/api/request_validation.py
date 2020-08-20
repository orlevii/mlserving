from validr import T, Compiler


def request_schema(schema: dict):
    def decorator(predictor_cls):
        s = T(schema)

        predictor_cls._schema_func = Compiler().compile(s)

        return predictor_cls

    return decorator


class RequestValidator:
    @staticmethod
    def validate_schema(predictor_cls, input_data):
        func = getattr(predictor_cls, '_schema_func', None)
        if func is not None:
            try:
                return func(input_data)
            except Exception as e:
                raise ValueError(f'Error in validating request-params, error: {e}')

        return input_data
