class WrapperException(Exception):
    def __init__(self, wrapper_name, message):
        self.wrapper_name = wrapper_name
        self.message = message

    def __str__(self):
        return f'WrapperException by {self.wrapper_name}: {message}'
