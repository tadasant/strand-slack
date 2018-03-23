from src.services.Service import Service


class ConvertTextToGFMService(Service):
    """Given text, convert to Github Flavored Markdown"""

    def __init__(self, text, slack_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper)
        self.text = text

    def execute(self):
        """Return the converted markdown"""
        self.logger.debug(f'Converting text to GFM: {repr(self.text)}')
        # TODO Vikas to implement
        return self.text
