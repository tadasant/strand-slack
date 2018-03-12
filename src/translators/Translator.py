from src import get_logger


class Translator:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def translate(self):
        raise NotImplementedError
