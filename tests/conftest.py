import pytest
from pytest_factoryboy import register

from src import create_app
from src.blueprints.slackapps.Factory import Factory
from tests.factories import BotFactory, BotSettingsFactory
from tests.testresources import TestSlackClient
from tests.testresources.TestPortalClient import TestPortalClient

register(BotFactory)
register(BotSettingsFactory)


@pytest.fixture
def app(portal_client, slack_client_class):
    app = create_app(portal_client=portal_client, SlackClientClass=slack_client_class)
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


@pytest.fixture(scope='session')
def portal_client():
    return TestPortalClient()


@pytest.fixture(scope='session')
def slack_client_class():
    return TestSlackClient
