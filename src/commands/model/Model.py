from copy import deepcopy


class Model:
    def as_dict(self):
        return deepcopy(vars(self))
