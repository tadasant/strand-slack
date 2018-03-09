from src.models.Model import Model


class Installation(Model):
    def __init__(self, access_token, bot_access_token, installer, bot_user_id):
        self.access_token = access_token
        self.installer = installer
        self.bot_access_token = bot_access_token
        self.bot_user_id = bot_user_id
