import pytest
from pytest_factoryboy import register

from app import app as myapp
from app.factory.Factory import Factory
from tests.factories import BotFactory

register(BotFactory)


@pytest.fixture
def app():
    return myapp


@pytest.fixture
def factory():
    factory = Factory()
    return factory


@pytest.fixture
def factory_with_bots(bot_factory):
    factory = Factory()
    return factory
