import pytest

from app import app as myapp


@pytest.fixture
def app():
    return myapp
