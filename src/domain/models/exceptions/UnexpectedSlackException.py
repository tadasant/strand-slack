class UnexpectedSlackException(Exception):
    """Raised when Slack sends a request with an unexpected (likely mis-modeled) payload"""

    def __init__(self, message):
        super().__init__()

        self.message = message

    def __str__(self):
        return self.message
