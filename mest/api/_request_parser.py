from cerberus import Validator


def validate_schema(input_data, schema) -> dict:
    v = Validator()
    if not v.validate(input_data, schema):
        raise ValueError('Error in validating request-params, errors: {}'.format(v.errors))

    return v.normalized(input_data)
