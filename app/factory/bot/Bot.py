from app.factory.bot.BotThread import BotThread


class Bot:
    def __init__(self, slack_team_name, slack_team_id, access_token, installer_id, bot_user_id, bot_access_token):
        self.slack_team_name = slack_team_name
        self.slack_team_id = slack_team_id
        self.access_token = access_token
        self.installer_id = installer_id
        self.bot_user_id = bot_user_id
        self.bot_access_token = bot_access_token
        self.bot_thread = None

    def start(self):
        if not self.bot_thread:
            self.bot_thread = BotThread()
            self.bot_thread.start()
            print(f'Bot in team "{self.slack_team_name}" started')
        else:
            if self.bot_thread.is_stopped:
                self.bot_thread.start()
                print(f'Bot in team "{self.slack_team_name}" started')
            else:
                print(f'Bot in team "{self.slack_team_name}" already started')
        return True

    def is_alive(self):
        return self.bot_thread and self.bot_thread.is_alive()

    def stop(self):
        if self.bot_thread and not self.bot_thread.is_stopped:
            self.bot_thread.stop()
            print(f'Bot in team "{self.slack_team_name}" stopped')
        else:
            print(f'Bot in team {self.slack_team_name} already stopped')

    def destroy(self):
        if self.bot_thread:
            if self.bot_thread.is_stopped:
                self.bot_thread.join()
            else:
                self.bot_thread.stop()
                self.bot_thread.join()
        print(f'Bot in team "{self.slack_team_name}" destroyed')
