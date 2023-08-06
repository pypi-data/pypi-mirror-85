import logging


def disable_logger(logger: logging.Logger, should_disable=True):
    def inner(func):
        def wrapper(*args, **kwargs):
            if should_disable:
                logger.disabled = True
                result = func(*args, **kwargs)
                logger.disabled = False
                return result
            else:
                return func(*args, **kwargs)

        return wrapper

    return inner
