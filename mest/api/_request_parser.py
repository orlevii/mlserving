from cerberus import Validator


def validate_schema(input_data, schema) -> dict:
    v = Validator()
    if not v.validate(input_data, schema):
        raise ValueError(f'Error in validating request-params, errors: {v.errors}')

    return v.normalized(input_data)
