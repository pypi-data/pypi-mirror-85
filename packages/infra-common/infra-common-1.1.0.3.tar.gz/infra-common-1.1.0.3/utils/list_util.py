import typing

import allure


@allure.step('Going to compare between {origin} and {array_to_compare}')
def compare_between_two_arrays(origin: typing.List, array_to_compare: typing.List, threshold: float) -> (typing.List,
                                                                                                         typing.List):
    origin_miss = []
    array_to_compare_miss = []
    for i in range(len(array_to_compare)):
        if origin[i] - array_to_compare[i] > threshold:
            origin_miss.append(origin[i])
            array_to_compare_miss.append(array_to_compare[i])
    return origin_miss, array_to_compare_miss
