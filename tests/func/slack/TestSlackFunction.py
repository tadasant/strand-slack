from tests.func.TestFunction import TestFunction


class TestSlackFunction(TestFunction):
    default_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
