class SlackCommunicationException(Exception):
    """Raise when there's a payload-related issue receiving a request/response from Slack"""

    def __init__(self, message=None):
        super().__init__()

        self.message = message

    def __repr__(self):
        return f'<{self.__class__}({self.__dict__})>'
