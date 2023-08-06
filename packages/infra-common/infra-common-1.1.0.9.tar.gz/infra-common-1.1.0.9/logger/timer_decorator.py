import logging
import timeit


def log_time(logger: logging.Logger):
    def inner(func):
        def wrapper(*args, **kwargs):
            start_time = timeit.default_timer()
            result = func(*args, **kwargs)
            elapsed = timeit.default_timer() - start_time
            logger.debug(f'function {func.__name__} took: {elapsed} seconds')
            return result

        return wrapper

    return inner
