class UnexpectedSlackException(Exception):
    def __init__(self, message):
        super()

        self.message = message

    def __str__(self):
        return self.message
