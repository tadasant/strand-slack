from app.factory.bot.Bot import Bot


class Factory:
    def __init__(self):
        self.bots = {}

    def create_bot(self, bot_settings):
        if self.bots.get(bot_settings.slack_team_id):
            return None

        bot = Bot(bot_settings)
        bot.start()
        self.bots.update({bot.slack_team_id: bot})
        return bot

    def get_bots(self):
        return [bot.as_dict() for slack_team_id, bot in self.bots.items()]

    def resume_bots(self):
        for slack_team_id, bot in self.bots.items():
            bot.resume()

    def pause_bots(self):
        for slack_team_id, bot in self.bots.items():
            bot.pause()

    def destroy_bots(self):
        for slack_team_id, bot in enumerate(self.bots):
            bot.destroy()
            self.bots.pop(slack_team_id)
