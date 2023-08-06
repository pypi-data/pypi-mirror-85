import pytest
from assertpy import assert_that

from common.utils import string_utils


@pytest.mark.infra
@pytest.mark.parametrize('version,expected_tuple', [('2.3.1', [2, 3, 1]),
                                                    ('1', [1, ]),
                                                    ])
def test_version_to_tuple(version: str, expected_tuple):
    assert_that(string_utils.version_to_tuple(version)).is_equal_to(expected_tuple)


@pytest.mark.infra
@pytest.mark.parametrize('version', [1, 1.1, {'1'}, {'1': 1}, ['list_type', ], ('1,1',)],
                         ids=['int', 'float', 'set', 'dict', 'list', 'tuple'])
def test_version_to_tuple_raises_exception_on_invalid_type(version: str, ):
    with pytest.raises(TypeError):
        string_utils.version_to_tuple(version)


@pytest.mark.infra
@pytest.mark.parametrize('version', ['a', '.1.1.1'])
def test_version_to_tuple_raises_exception_on_invalid_format(version: str, ):
    with pytest.raises(ValueError):
        string_utils.version_to_tuple(version)


@pytest.mark.infra
def test_version_to_tuple_remove_letters_does_not_bypass_other_exceptions():
    with pytest.raises(ValueError):
        string_utils.version_to_tuple('.1.2a', ignore_non_digits_or_dots=True)


@pytest.mark.infra
def test_version_to_tuple_ignore_non_digits_or_dots_parameter():
    version_str = '2a.1b.3p.145abcdefg.-1$%!^\\*&()'
    expected_result = [2, 1, 3, 145, 1]
    result = string_utils.version_to_tuple(version_str, ignore_non_digits_or_dots=True)
    assert_that(result).is_equal_to(expected_result)


@pytest.mark.infra
@pytest.mark.parametrize(argnames=['input_str', 'expected'],
                         argvalues=[['a,1/2.3.bb%4.5', '12345'],
                                    [None, None],
                                    ['', '']])
def test_remove_non_digit_characters(input_str, expected):
    result = string_utils.remove_non_digit_characters(input_str)
    assert_that(result).is_equal_to(expected)
