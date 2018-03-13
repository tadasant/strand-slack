from src.utilities.logging import get_logger


class Translator:
    def __init__(self, slack_client_wrapper=None, strand_api_client_wrapper=None):
        self.logger = get_logger(self.__class__.__name__)
        self.slack_client_wrapper = slack_client_wrapper
        self.strand_api_client_wrapper = strand_api_client_wrapper

    def translate(self):
        raise NotImplementedError
