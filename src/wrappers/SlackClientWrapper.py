from slackclient import SlackClient

from src.common.logging import get_logger


class SlackClientWrapper:
    def __init__(self, tokens_by_team_id, log_file):
        self.tokens_by_team_id = tokens_by_team_id if tokens_by_team_id else {}
        self.logger = get_logger('SlackClientWrapper', log_file)

    def add_tokens(self, tokens, team_id):
        self.tokens_by_team_id[team_id] = tokens

    def do_some_action(self, team_id):
        """Illustrative template (remove later)"""
        if team_id not in self.tokens_by_team_id:
            raise Exception  # TODO make a custom error type
        client = SlackClient(token=self.tokens_by_team_id[team_id].bot_access_token)
        # client.api_call....
