class Model:
    def __repr__(self):
        return f'<{self.__class__}({self.__dict__})>'

    def __eq__(self, other):
        if all(k is not None for k in self.__dict__.keys()):
            # All values are set, sufficient to determine equality
            return self.__dict__ == other.__dict__
        return False
