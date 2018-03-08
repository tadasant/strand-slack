import threading

import pytest
from pytest_factoryboy import register

from src import create_app
from src.common.logging import get_logger
from src.config import config
from src.domain.repositories.SlackAgentRepository import slack_agent_repository as slack_agent_repository_global
from tests.factories.coreapifactories import SlackAgentFactory
from tests.factories.slackfactories import InteractiveComponentRequestFactory
from tests.testresources.TestCoreApiClient import TestCoreApiClient
from tests.testresources.TestSlackClient import TestSlackClient, clear_slack_state
from tests.utils import wait_until

register(SlackAgentFactory)
register(InteractiveComponentRequestFactory)


# Maintenance

@pytest.fixture(scope='session', autouse=True)
def init_tempdir(tmpdir_factory):
    assert tmpdir_factory.getbasetemp()


@pytest.fixture(scope='session')
def client(app):
    client = app.test_client()
    return client


@pytest.fixture(autouse=True)
def wait_for_threads():
    yield
    wait_until(condition=lambda: len(threading.enumerate()) <= 4, timeout=5)


@pytest.fixture(autouse=True)
def log_test_start():
    logger = get_logger('Fixtures')
    logger.info('******** TEST START ********')
    yield
    logger.info('******** TEST END ********')


# Core

@pytest.fixture(scope='session')
def app(core_api_client_factory, slack_client_class):
    app = create_app(core_api_client=core_api_client_factory, SlackClientClass=slack_client_class,
                     slack_verification_tokens=config['SLACK_VERIFICATION_TOKENS'],
                     core_api_verification_token=config['CORE_API_VERIFICATION_TOKEN'])
    app.testing = True
    return app


@pytest.fixture
def slack_agent_repository():
    yield slack_agent_repository_global
    slack_agent_repository_global.clear()


# Wrappers & Clients

@pytest.fixture(scope='session')
def core_api_client_factory():
    return TestCoreApiClient()


@pytest.fixture
def core_api_client(core_api_client_factory):
    core_api_client_factory.clear_responses()
    yield core_api_client_factory
    core_api_client_factory.clear_responses()


@pytest.fixture
def slack_client():
    """Simulates Slack's actual state. Include fixture if using Slack's returned values."""
    clear_slack_state()
    yield
    clear_slack_state()


@pytest.fixture(scope='session')
def slack_client_class():
    """Type of client to make on a per-call basis throughout tests"""
    return TestSlackClient
