import threading
import time
from copy import deepcopy


def wait_until(condition, interval=0.1, timeout=2, *args, **kwargs):
    start = time.time()
    result = condition(*args, **kwargs)
    while not result and time.time() - start < timeout:
        time.sleep(interval)
        result = condition(*args, **kwargs)
    return result


def wait_for_extra_threads_to_die(baseline_count=1, timeout=5):
    return wait_until(condition=lambda: len(threading.enumerate()) <= baseline_count, timeout=timeout)


def assert_values_in_call_args_list(params_to_expecteds, call_args_list, expect_succeed=True):
    """
    Asserts that a subset of each item in params_to_expecteds exists in the call args list.

    If expect_succeed is False, will return the inverse. Useful when checking to make sure calls DIDN'T happen.

    :param params_to_expecteds: e.g. [{'paramname': 'expectedval', 'param2name': 'expected2val}]
    """
    params_to_actuals = [x[1] for x in call_args_list]
    original_params_to_expecteds = deepcopy(params_to_expecteds)
    for i, expected in enumerate(original_params_to_expecteds):
        for j, actual in enumerate(params_to_actuals):
            if all(item in actual.items() for item in expected.items()):
                params_to_expecteds[i] = None
                params_to_actuals[j] = {}
                break

    condition = len([x for x in params_to_expecteds if x is not None]) == 0
    assert condition if expect_succeed else not condition, f'{params_to_expecteds} vs. {params_to_actuals}'
