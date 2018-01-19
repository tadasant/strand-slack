from app.factory.bot.Bot import Bot


class Factory:
    def __init__(self):
        self.bots = []

    def create_bot(self, slack_team_name, slack_team_id, access_token, installer_id, bot_user_id, bot_access_token):
        bot = Bot(slack_team_name, slack_team_id, access_token, installer_id, bot_user_id, bot_access_token)
        bot.start()
        self.bots.append(bot)

    def get_bots(self):
        bots = []
        for bot in self.bots:
            bots.append({'bot': bot.slack_team_name, 'is_alive': bot.is_alive()})
        return bots

    def start_bots(self):
        for bot in self.bots:
            if bot.is_stopped:
                bot.start()

    def stop_bots(self):
        for bot in self.bots:
            bot.stop()

    def destroy_bots(self):
        for idx, bot in enumerate(self.bots):
            bot.destroy()
            self.bots.pop(idx)
