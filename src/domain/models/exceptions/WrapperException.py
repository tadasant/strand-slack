class WrapperException(Exception):
    def __init__(self, wrapper_name, message):
        super(WrapperException, self).__init__(message)

        self.wrapper_name = wrapper_name
        self.message = message

    def __str__(self):
        return f'{self.wrapper_name}\n\t{self.message}'