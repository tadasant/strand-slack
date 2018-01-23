from slackclient import SlackClient

from src.common.logging import get_logger


class SlackClientWrapper:
    def __init__(self, bot_token, oauth_token, log_file):
        self.bot_user_client = SlackClient(bot_token)
        self.app_client = SlackClient(oauth_token)
        self.logger = get_logger('SlackClientWrapper', log_file)
