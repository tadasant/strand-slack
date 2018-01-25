import factory

from src.blueprints.portal.bot.Bot import Bot
from src.blueprints.portal.bot.BotSettings import BotSettings
from src.domain.models import SlackApplicationInstallation
from src.domain.models import SlackTeam
from src.domain.models import SlackUser


class BotSettingsFactory(factory.Factory):
    class Meta:
        model = BotSettings

    slack_team_name = factory.Faker('company')
    slack_team_id = factory.Faker('ean8')
    access_token = factory.Faker('md5')
    installer_id = factory.Faker('ean8')
    bot_user_id = factory.Faker('ean8')
    bot_access_token = factory.Faker('md5')


class BotFactory(factory.Factory):
    class Meta:
        model = Bot

    bot_settings = factory.SubFactory(BotSettingsFactory)


class SlackTeamFactory(factory.Factory):
    class Meta:
        model = SlackTeam

    id = factory.Faker('ean8')


class SlackUserFactory(factory.Factory):
    class Meta:
        model = SlackUser

    id = factory.Faker('ean8')


class SlackApplicationInstallationFactory(factory.Factory):
    class Meta:
        model = SlackApplicationInstallation

    bot_access_token = factory.Faker('md5')
    access_token = factory.Faker('md5')
    slack_team = SlackTeamFactory
    installer = SlackUserFactory
    is_active = False
