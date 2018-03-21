class SLAException(Exception):
    """Generic exception for local exception types"""

    def __init__(self, message=None):
        super().__init__()

        self.message = message

    def __repr__(self):
        return f'<{self.__class__}({self.__dict__})>'
