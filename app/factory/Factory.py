from app.factory.bot.Bot import Bot
from app import app


class Factory:
    def __init__(self):
        self.bots = []

    def create_bot(self, slack_team_name, slack_team_id, access_token, installer_id, bot_user_id, bot_access_token):
        bot = Bot(slack_team_name, slack_team_id, access_token, installer_id, bot_user_id, bot_access_token)
        bot.start()

        app.logger.info(f'Created bot in team "{bot.slack_team_name}"')

        self.bots.append(bot)

    def get_bots(self):
        bots = []
        for bot in self.bots:
            bots.append({'bot': bot.slack_team_name, 'is_alive': bot.is_alive()})
        return bots

    def start_bots(self):
        app.logger.info(f'Starting {len(self.bots)} bots')

        for bot in self.bots:
            if bot.is_stopped:
                bot.start()

    def stop_bots(self):
        app.logger.info(f'Stopping {len(self.bots)} bots')

        for bot in self.bots:
            bot.stop()

    def destroy_bots(self):
        app.logger.info(f'Destroying {len(self.bots)} bots')

        for idx, bot in enumerate(self.bots):
            bot.destroy()
            self.bots.pop(idx)
