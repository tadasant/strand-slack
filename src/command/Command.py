from src.common.logging import get_logger


class Command:
    def __init__(self, slack_client_wrapper=None, portal_client_wrapper=None):
        self.slack_client_wrapper = slack_client_wrapper
        self.portal_client_wrapper = portal_client_wrapper
        self.logger = get_logger(self.__class__.__name__)

    def execute(self):
        raise NotImplementedError
