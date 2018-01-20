import pytest
from pytest_factoryboy import register

from app import create_app
from app.factory.Factory import Factory
from tests.factories import BotFactory, BotSettingsFactory

register(BotFactory)
register(BotSettingsFactory)


@pytest.fixture
def app():
    app = create_app()
    app.config.update(TESTING=True)
    return app


@pytest.fixture()
def client(app):
    client = app.test_client()
    return client


@pytest.fixture
def factory():
    factory = Factory()
    return factory
