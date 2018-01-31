import pytest


@pytest.mark.usefixtures('client_class')  # pytest-flask's client_class adds self.client
class TestFunction:
    pass
