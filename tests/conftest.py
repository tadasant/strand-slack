import threading

import pytest
from pytest_factoryboy import register

from src import create_app
from src.config import config
from src.utilities.database import metadata, engine, Session
from src.utilities.logging import get_logger
from tests.factories.slackfactories import SlackOauthAccessResponseFactory, SlackUserFactory, SlackEventRequestFactory,\
    SlackInteractiveComponentRequestFactory
from tests.testresources.TestSlackClient import TestSlackClient
from tests.testresources.TestStrandApiClient import TestStrandApiClient
from tests.utils.asserting import wait_until

register(SlackOauthAccessResponseFactory)
register(SlackUserFactory)
register(SlackEventRequestFactory)
register(SlackInteractiveComponentRequestFactory)


# Maintenance

@pytest.fixture(scope='session', autouse=True)
def init_tempdir(tmpdir_factory):
    assert tmpdir_factory.getbasetemp()


@pytest.fixture(autouse=True)
def wait_for_threads(baseline_thread_count):
    yield
    wait_until(condition=lambda: threading.active_count() <= baseline_thread_count, timeout=5)


@pytest.fixture(autouse=True)
def log_test_start():
    logger = get_logger('Fixtures')
    logger.info('******** TEST START ********')
    yield
    logger.info('******** TEST END ********')


@pytest.fixture(scope='function')
def baseline_thread_count():
    return threading.active_count()


# Core application resources

@pytest.fixture(scope='session')
def app(strand_api_client_factory, slack_client_class):
    app = create_app(strand_api_client=strand_api_client_factory, SlackClientClass=slack_client_class,
                     slack_verification_tokens=config['SLACK_VERIFICATION_TOKENS'],
                     strand_api_verification_token=config['STRAND_API_VERIFICATION_TOKEN'],
                     ui_host=config['STRAND_UI_HOST'])
    app.testing = True
    return app


@pytest.fixture(scope='session')
def client(app):
    client = app.test_client()
    return client


@pytest.fixture(scope='function', autouse=True)
def db_session():
    metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
    metadata.drop_all(engine)


# Wrappers & Clients

@pytest.fixture(scope='session')
def strand_api_client_factory():
    return TestStrandApiClient()


@pytest.fixture
def strand_api_client(strand_api_client_factory):
    yield strand_api_client_factory


@pytest.fixture(scope='session')
def slack_client_class():
    """Type of client to make on a per-call basis throughout tests"""
    return TestSlackClient
