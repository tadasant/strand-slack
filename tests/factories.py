import factory

from app.factory.bot.Bot import Bot


class BotFactory(factory.Factory):
    class Meta:
        model = Bot

    slack_team_name = None
    slack_team_id = None
    access_token = None
    installer_id = None
    bot_user_id = None
    bot_access_token = None
    bot_thread = None
