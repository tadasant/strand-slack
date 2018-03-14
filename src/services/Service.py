from src.utilities.logging import get_logger


class Service:
    """Parent for all services"""

    def __init__(self, slack_client_wrapper=None, strand_api_client_wrapper=None):
        self.slack_client_wrapper = slack_client_wrapper
        self.strand_api_client_wrapper = strand_api_client_wrapper
        self.logger = get_logger(self.__class__.__name__)

    def execute(self, **kwargs):
        raise NotImplementedError
