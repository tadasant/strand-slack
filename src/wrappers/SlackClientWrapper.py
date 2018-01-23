from src.common.logging import get_logger


class SlackClientWrapper:
    """Manages all outgoing interaction with Slack APIs"""

    def __init__(self, tokens_by_team_id, SlackClientClass):
        self.tokens_by_team_id = tokens_by_team_id if tokens_by_team_id else {}
        self.SlackClientClass = SlackClientClass
        self.logger = get_logger('SlackClientWrapper')

    def set_tokens(self, tokens, team_id):
        """Register tokens for a new team that the wrapper can leverage (new or updated)"""
        self.tokens_by_team_id[team_id] = tokens

    def do_some_action(self, team_id):
        """Illustrative template (remove later)"""
        if team_id not in self.tokens_by_team_id:
            raise Exception  # TODO make a custom error type
        # TODO retry logic
        self.SlackClientClass(token=self.tokens_by_team_id[team_id].bot_access_token)
        # client.api_call....
