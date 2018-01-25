from src import slack_agent_repository
from src.common.logging import get_logger


class SlackClientWrapper:
    """Manages all outgoing interaction with Slack APIs"""

    def __init__(self, SlackClientClass):
        self.SlackClientClass = SlackClientClass
        self.logger = get_logger('SlackClientWrapper')

    def do_some_action(self, team_id):
        """Illustrative template (remove later)"""
        if team_id not in slack_agent_repository.slack_agents_by_team_id:
            raise Exception  # TODO make a custom error type
        # TODO retry logic
        token = slack_agent_repository.slack_agents_by_team_id[team_id].slack_application_installation.bot_access_token
        self.SlackClientClass(token=token)
        # client.api_call....
