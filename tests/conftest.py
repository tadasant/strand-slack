import pytest
from pytest_factoryboy import register

from src import create_app
from src import slack_agent_repository as slack_agent_repository_global
from tests.factories import SlackAgentFactory
from tests.testresources.TestSlackClient import TestSlackClient
from tests.testresources.TestPortalClient import TestPortalClient

register(SlackAgentFactory)


# Maintenance

@pytest.fixture(scope='session', autouse=True)
def init_tempdir(tmpdir_factory):
    assert tmpdir_factory.getbasetemp()


@pytest.fixture(scope='session')
def client(app):
    client = app.test_client()
    return client


# Core

@pytest.fixture(scope='session')
def app(portal_client_factory):
    app = create_app(portal_client=portal_client_factory, SlackClientClass=TestSlackClient)
    app.testing = True
    return app


@pytest.fixture
def slack_agent_repository():
    yield slack_agent_repository_global
    slack_agent_repository_global.clear()


# Wrappers & Clients

@pytest.fixture(scope='session')
def portal_client_factory():
    return TestPortalClient()


@pytest.fixture
def portal_client(portal_client_factory):
    yield portal_client_factory
    portal_client_factory.clear_response()
