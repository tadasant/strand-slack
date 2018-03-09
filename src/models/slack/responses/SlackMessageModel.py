from copy import deepcopy

from src.models.Model import Model


class SlackMessageModel(Model):
    # TODO replace as_dict with serializing funcs
    def as_dict(self):
        return deepcopy(vars(self))
