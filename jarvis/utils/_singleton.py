from functools import wraps


def singleton():
    def decorator(cls):
        cls.instance = None

        @wraps(cls)
        def wrapper():
            if cls.instance is None:
                cls.instance = cls()

            return cls.instance

        wrapper.original_class = cls
        return wrapper

    return decorator
