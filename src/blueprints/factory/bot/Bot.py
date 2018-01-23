from src.blueprints.factory.bot.BotThread import BotThread


class Bot:
    def __init__(self, bot_settings):
        self.slack_team_name = bot_settings.slack_team_name
        self.slack_team_id = bot_settings.slack_team_id
        self.access_token = bot_settings.access_token
        self.installer_id = bot_settings.installer_id
        self.bot_user_id = bot_settings.bot_user_id
        self.bot_access_token = bot_settings.bot_access_token
        self.bot_thread = BotThread()

    def start(self):
        if not self.bot_thread.is_alive():
            self.bot_thread.start()
            print(f'Bot in team "{self.slack_team_name}" started')

    def is_alive(self):
        return self.bot_thread and self.bot_thread.is_alive() and not self.bot_thread.is_paused

    def pause(self):
        if self.bot_thread and not self.bot_thread.is_paused:
            self.bot_thread.pause()
            print(f'Bot in team "{self.slack_team_name}" paused')
        else:
            print(f'Bot in team {self.slack_team_name} already paused')

    def resume(self):
        if self.bot_thread.is_paused:
            self.bot_thread.resume()
            print(f'Bot in team "{self.slack_team_name}" resumed')
        else:
            print(f'Bot in team "{self.slack_team_name}" already running')

    def destroy(self):
        if self.bot_thread.is_stopped:
            self.bot_thread.join()
        else:
            self.bot_thread.stop()
            self.bot_thread.join()

        print(f'Bot in team "{self.slack_team_name}" destroyed')

    def as_dict(self):
        return {'slack_team_id': self.slack_team_id,
                'slack_team_name': self.slack_team_name,
                'is_alive': self.is_alive()}
