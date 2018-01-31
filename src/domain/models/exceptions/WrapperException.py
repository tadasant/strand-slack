class WrapperException(Exception):
    def __init__(self, wrapper_name, message, errors=None):
        super().__init__()

        self.wrapper_name = wrapper_name
        self.message = message
        self.errors = errors

    def __str__(self):
        return f'{self.wrapper_name}\n\t{self.message}'
