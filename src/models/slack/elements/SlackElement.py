from src.models.Model import Model


class SlackElement(Model):
    def __init__(self, label, name, type, max_length=None, hint=None):
        self.label = label
        self.name = name
        self.type = type
        if max_length:
            self.max_length = max_length
        if hint:
            self.hint = hint
