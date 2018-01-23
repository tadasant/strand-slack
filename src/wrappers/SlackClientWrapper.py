from slackclient import SlackClient

from src.common.logging import get_logger


class SlackClientWrapper:
    def __init__(self, tokens_by_team_id, log_file):
        self.tokens_by_team_id = tokens_by_team_id
        self.logger = get_logger('SlackClientWrapper', log_file)

    def do_some_action(self, team_id):
        """Illustrative template (remove later)"""
        client = SlackClient(token=self.tokens_by_team_id[team_id].bot_access_token)
        # client.api_call....
