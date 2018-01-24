from src.blueprints.slackapps.bot.Bot import Bot
from src.exceptions import BotAlreadyExists


class Factory:
    def __init__(self):
        self.bots = {}

    def create_bot(self, bot_settings):
        if self.bots.get(bot_settings.slack_team_id):
            raise BotAlreadyExists

        bot = Bot(bot_settings)
        bot.start()
        self.bots.update({bot.slack_team_id: bot})
        return bot

    def get_bots(self):
        return [bot.as_dict() for bot in self.bots.values()]

    def resume_bots(self):
        for bot in self.bots.values():
            bot.resume()

    def pause_bots(self):
        for bot in self.bots.values():
            bot.pause()

    def destroy_bots(self):
        for slack_team_id, bot in self.bots.items():
            bot.destroy()
            self.bots.pop(slack_team_id)
