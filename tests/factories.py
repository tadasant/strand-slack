import factory

from src.blueprints.slackapps.bot.Bot import Bot
from src.blueprints.slackapps.bot.BotSettings import BotSettings
from src.models.SlackApplicationInstallation import SlackApplicationInstallation


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


class SlackApplicationInstallationFactory(factory.Factory):
    class Meta:
        model = SlackApplicationInstallation

    bot_access_token = factory.Faker('md5')
    access_token = factory.Faker('md5')
