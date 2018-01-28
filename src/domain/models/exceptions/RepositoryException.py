class RepositoryException(Exception):
    def __init__(self, object_name, message):
        super()

        self.object_name = object_name
        self.message = message

    def __str__(self):
        return f'{self.object_name}\n\t{self.message}'
