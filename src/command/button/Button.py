from copy import deepcopy


class Button:
    def __init__(self, fallback, callback_id, color, attachment_type, actions):
        self.fallback = fallback
        self.callback_id = callback_id
        self.color = color
        self.attachment_type = attachment_type
        self.actions = actions

    def as_dict(self):
        result = deepcopy(vars(self))
        result['actions'] = [vars(action) for action in self.actions]
        return result
