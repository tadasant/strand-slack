from factory import Faker

"""Wraps Faker so that we can generate primitive non-object values"""


class PrimitiveFaker(Faker):
    def __init__(self, provider, **kwargs):
        super().__init__(provider, **kwargs)
        self.value = self.generate({})

    def __str__(self):
        return str(self.value)
