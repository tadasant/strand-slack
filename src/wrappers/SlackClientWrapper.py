from src.common.logging import get_logger


class SlackClientWrapper:
    """Manages all outgoing interaction with Slack APIs"""

    def __init__(self, installations_by_team_id, SlackClientClass):
        self.installations_by_team_id = installations_by_team_id if installations_by_team_id else {}
        self.SlackClientClass = SlackClientClass
        self.logger = get_logger('SlackClientWrapper')

    def set_installation(self, installation, team_id):
        """Register installations for a new team that the wrapper can leverage (new or updated)"""
        self.installations_by_team_id[team_id] = installation

    def do_some_action(self, team_id):
        """Illustrative template (remove later)"""
        if team_id not in self.installations_by_team_id:
            raise Exception  # TODO make a custom error type
        # TODO retry logic
        self.SlackClientClass(token=self.installations_by_team_id[team_id].bot_access_token)
        # client.api_call....
