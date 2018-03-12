from src.utilities.logging import get_logger


class Command:
    """Parent for all commands procedures"""

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def execute(self):
        raise NotImplementedError
