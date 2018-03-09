from copy import deepcopy

from src.models.SlackModel import SlackModel


class SlackMessageModel(SlackModel):
    # TODO replace as_dict with serializing funcs
    def as_dict(self):
        return deepcopy(vars(self))
