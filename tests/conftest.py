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
    return app


@pytest.fixture
def factory():
    factory = Factory()
    return factory


@pytest.fixture
def factory_with_bots(bot_factory):
    factory = Factory()
    bot_one = bot_factory.build()
    factory.create_bot(bot_one.slack_team_name, bot_one.slack_team_id,
                       bot_one.access_token, bot_one.installer_id,
                       bot_one.bot_user_id, bot_one.bot_access_token)
    bot_two = bot_factory.build()
    factory.create_bot(bot_two.slack_team_name, bot_two.slack_team_id,
                       bot_two.access_token, bot_two.installer_id,
                       bot_two.bot_user_id, bot_two.bot_access_token)
    return factory
