import factory

from app.factory.bot.Bot import Bot


class BotFactory(factory.Factory):
    class Meta:
        model = Bot

    slack_team_name = factory.Faker('company')
    slack_team_id = factory.Faker('ean8')
    access_token = factory.Faker('md5')
    installer_id = factory.Faker('ean8')
    bot_user_id = factory.Faker('ean8')
    bot_access_token = factory.Faker('md5')
