import pytest
from pytest_factoryboy import register

from src import create_app
from src.blueprints.portal.Factory import Factory
from tests.factories import BotFactory, BotSettingsFactory, SlackApplicationInstallationFactory
from tests.testresources import TestSlackClient
from tests.testresources.TestPortalClient import TestPortalClient

register(BotFactory)
register(BotSettingsFactory)
register(SlackApplicationInstallationFactory)


@pytest.fixture(scope='session', autouse=True)
def init_tempdir(tmpdir_factory):
    assert tmpdir_factory.getbasetemp()


@pytest.fixture(scope='session')
def app(portal_client_factory):
    app = create_app(portal_client=portal_client_factory, SlackClientClass=TestSlackClient)
    app.testing = True
    return app


@pytest.fixture(scope='session')
def client(app):
    client = app.test_client()
    return client


@pytest.fixture
def factory():
    factory = Factory()
    return factory


@pytest.fixture(scope='session')
def portal_client_factory():
    return TestPortalClient()


@pytest.fixture
def portal_client(portal_client_factory):
    yield portal_client_factory
    portal_client_factory.clear_response()
