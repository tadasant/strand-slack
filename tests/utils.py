import threading
import time


def wait_until(condition, interval=0.1, timeout=2, *args, **kwargs):
    start = time.time()
    result = condition(*args, **kwargs)
    while not result and time.time() - start < timeout:
        time.sleep(interval)
        result = condition(*args, **kwargs)
    return result


def wait_for_extra_threads_to_die(baseline_count=4, timeout=5):
    return wait_until(condition=lambda: len(threading.enumerate()) <= baseline_count, timeout=timeout)
