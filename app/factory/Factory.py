from app.factory.bot.Bot import Bot


class Factory:
    def __init__(self):
        self.bots = {}

    def create_bot(self, bot_settings):
        if self.bots.get(bot_settings.SLACK_TEAM_ID):
            raise Exception('Bot already exists')

        bot = Bot(bot_settings)
        bot.start()
        self.bots[bot.slack_team_id] = bot

        return bot

    def get_bots(self):
        bots = []
        for slack_team_id, bot in self.bots.items():
            bots.append(bot.as_dict())
        return bots

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
