from cerberus import Validator


def validate_params(input_data, schema):
    v = Validator()
    v.validate(input_data, schema)
    return v.normalized(input_data)
