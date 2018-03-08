from src.utilities.logging import get_logger


class Command:
    """Parent for all commands procedures"""

    def __init__(self, slack_team_id, slack_client_wrapper=None, core_api_client_wrapper=None):
        self.slack_team_id = slack_team_id
        self.slack_client_wrapper = slack_client_wrapper
        self.core_api_client_wrapper = core_api_client_wrapper
        self.logger = get_logger(self.__class__.__name__)

    def execute(self):
        raise NotImplementedError
