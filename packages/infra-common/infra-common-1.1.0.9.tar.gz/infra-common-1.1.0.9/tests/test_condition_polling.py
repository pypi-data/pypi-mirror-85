from typing import Callable

import pytest
from assertpy import assert_that

from common.polling import condition_polling


# noinspection PyTypeChecker
@pytest.mark.infra
@pytest.mark.parametrize('polling_func,expected_exception',
                         [(condition_polling.poll, TimeoutError),
                          (condition_polling.assert_poll, AssertionError)])
def test_polling_ignores_exception(polling_func: Callable, expected_exception):
    with pytest.raises(Exception) as e:
        polling_func(func=lambda: exec('raise(Exception("Test failed))'), ignore_exceptions=Exception,
                     timeout_in_sec=0.002, sleep_time_sec=0.001)
    assert_that(e.value).is_instance_of(expected_exception)


@pytest.mark.infra
@pytest.mark.parametrize('polling_func', [condition_polling.poll, condition_polling.assert_poll])
def test_polling_does_not_ignore_errors_by_default(polling_func):
    with pytest.raises(Exception) as e:
        polling_func(func=lambda: exec('raise TabError("This should be thrown")'),
                     timeout_in_sec=0.002, sleep_time_sec=0.001)
    assert_that(e.value).is_instance_of(TabError)


# noinspection PyTypeChecker
@pytest.mark.infra
@pytest.mark.parametrize('polling_func', [condition_polling.poll, condition_polling.assert_poll])
def test_polling_ignores_only_exceptions_of_given_types(polling_func):
    with pytest.raises(Exception) as e:
        polling_func(func=lambda: exec('raise TabError("This should be thrown")'),
                     ignore_exceptions=RecursionError,
                     timeout_in_sec=0.002, sleep_time_sec=0.001)
    assert_that(e.value).is_instance_of(TabError)


@pytest.mark.infra
@pytest.mark.parametrize('expected_value', [1, 'dummy', 0, None])
def test_polling_with_value_returns_actual_value(expected_value):
    value = condition_polling.poll_with_value(done_condition=lambda x: True, func=lambda x: x, args=(expected_value,))
    assert_that(value).is_equal_to(expected_value)


@pytest.mark.infra
@pytest.mark.parametrize('polling_func,expected_exception',
                         [(condition_polling.poll, TimeoutError),
                          (condition_polling.assert_poll, AssertionError)])
@pytest.mark.parametrize('exception_type', ['RecursionError', 'IOError'])
def test_polling_ignores_multiple_exceptions(polling_func: Callable, exception_type, expected_exception):
    with pytest.raises(Exception) as e:
        polling_func(func=lambda: exec(f'raise {exception_type}("This should be thrown")'),
                     ignore_exceptions=(RecursionError, IOError),
                     timeout_in_sec=0.002, sleep_time_sec=0.001)
    assert_that(e.value).is_instance_of(expected_exception)


@pytest.mark.infra
def test_assert_poll_with_value_raises_assertion_error():
    with pytest.raises(AssertionError) as e:
        condition_polling.assert_poll_with_value(done_condition=lambda x: False, func=lambda: "dummy",
                                                 sleep_time_in_sec=0.001, timeout_in_sec=0.002,
                                                 timeout_msg='Test passed')
    assert_that(e.value.args).contains_only('Test passed')


@pytest.mark.infra
def test_assert_poll_raises_assertion_error():
    with pytest.raises(AssertionError) as e:
        condition_polling.assert_poll(func=lambda: False, timeout_in_sec=0.001, sleep_time_sec=0.0005,
                                      timeout_msg='Test passed')
        assert_that(e.value.args).contains_only('Test passed')
