from factory import Faker


class PrimitiveFaker(Faker):
    """Wraps Faker so that we can generate primitive non-object values"""

    def __init__(self, provider, **kwargs):
        super().__init__(provider, **kwargs)
        self.value = self.generate({})

    def __str__(self):
        return str(self.value)
