class UnauthorizedException(Exception):
    """Raised when caller is not an authenticated user with appropriate authorization"""

    def __init__(self, message):
        super().__init__()

        self.message = message

    def __repr__(self):
        return f'<{self.__class__}({self.__dict__})>'
