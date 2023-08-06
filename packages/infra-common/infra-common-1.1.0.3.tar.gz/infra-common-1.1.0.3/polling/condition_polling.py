import time
import typing
from datetime import datetime

from common.logger import log_wrapper
from common.logger.disable_decorator import disable_logger

logger = log_wrapper.logger()


def poll(func: typing.Callable[..., bool], args: tuple = (), sleep_time_sec: float = 0.5, timeout_in_sec: float = 60,
         timeout_msg: str = 'timeout', ignore_exceptions: typing.Tuple = (), disable_log=False) -> None:
    if not is_condition_true(func=func, args=args, sleep_time_in_sec=sleep_time_sec, timeout_in_sec=timeout_in_sec,
                             ignore_exceptions=ignore_exceptions, disable_log=disable_log):
        raise TimeoutError(timeout_msg)


def is_condition_true(func: typing.Callable[..., bool], args: tuple = (), sleep_time_in_sec: float = 0.5,
                      timeout_in_sec: float = 60,
                      ignore_exceptions: typing.Tuple = (), disable_log=False) -> bool:
    is_successful, polling_result = _inner_poll_with_value(done_condition=lambda x: x, func=func, args=args,
                                                           sleep_time_in_sec=sleep_time_in_sec,
                                                           timeout_in_sec=timeout_in_sec,
                                                           ignore_exceptions=ignore_exceptions, disable_log=disable_log)
    return is_successful


def poll_with_value(done_condition: typing.Callable[..., bool], func: typing.Callable, args: tuple = (),
                    sleep_time_in_sec: float = 0.5,
                    timeout_in_sec: float = 60,
                    ignore_exceptions: typing.Tuple = (), timeout_msg: str = 'timeout') -> object:
    is_successful, polling_result = _inner_poll_with_value(done_condition=done_condition, func=func, args=args,
                                                           sleep_time_in_sec=sleep_time_in_sec,
                                                           timeout_in_sec=timeout_in_sec,
                                                           ignore_exceptions=ignore_exceptions)
    if not is_successful:
        raise TimeoutError(timeout_msg)
    return polling_result


def _inner_poll_with_value(done_condition: typing.Callable[..., bool], func: typing.Callable, args: tuple = (),
                           sleep_time_in_sec: float = 0.5,
                           timeout_in_sec: float = 60,
                           ignore_exceptions: typing.Tuple = (), disable_log: bool = False) -> typing.Tuple[
    bool, typing.Optional[object]]:
    logger.debug(f'running {func.__name__} going to wait for condition for {timeout_in_sec} seconds')

    @disable_logger(logger=logger, should_disable=disable_log)
    def __inner_poll():
        start_time = time.time()
        while time.time() - start_time < timeout_in_sec:
            try:
                logger.debug(f'checking condition: {func.__name__}')
                function_value = func(*args)
                if done_condition(function_value):
                    return True, function_value
            except Exception as e:
                if isinstance(e, ignore_exceptions):
                    logger.debug(f'Got exception while polling on condition, exception is <{str(e)}>')
                else:
                    raise e
            time.sleep(sleep_time_in_sec)

        return False, None

    return __inner_poll()


def assert_poll(func: typing.Callable[..., bool], args: tuple = (), sleep_time_sec: float = 0.5,
                timeout_in_sec: float = 60, timeout_msg: str = 'timeout', ignore_exceptions: typing.Tuple = ()) -> None:
    if not is_condition_true(func=func, args=args, sleep_time_in_sec=sleep_time_sec, timeout_in_sec=timeout_in_sec,
                             ignore_exceptions=ignore_exceptions):
        raise AssertionError(timeout_msg)


def assert_poll_with_value(done_condition: typing.Callable[..., bool], func: typing.Callable, args: tuple = (),
                           sleep_time_in_sec: float = 0.5,
                           timeout_in_sec: float = 60,
                           ignore_exceptions: typing.Tuple = (), timeout_msg: str = 'timeout') -> object:
    is_successful, polling_result = _inner_poll_with_value(done_condition=done_condition, func=func, args=args,
                                                           sleep_time_in_sec=sleep_time_in_sec,
                                                           timeout_in_sec=timeout_in_sec,
                                                           ignore_exceptions=ignore_exceptions)
    if not is_successful:
        raise AssertionError(timeout_msg)
    return polling_result


def change_timeout_by_time_of_day(timeout):
    now = datetime.utcnow().hour
    if int(now) > 17 or int(now) < 4:
        return timeout * 2
    return timeout
