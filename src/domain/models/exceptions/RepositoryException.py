class RepositoryException(Exception):
    def __init__(self, object_name, message):
        super(RepositoryException, self).__init__(message)

        self.object_name = object_name
        self.message = message

    def __str__(self):
        return f'{self.object_name}\n\t{self.message}'
