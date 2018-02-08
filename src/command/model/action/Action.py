from src.command.model.Model import Model


class Action(Model):
    """Includes buttons"""

    def __init__(self, name, text, type, value, style=None, confirm=None):
        self.name = name
        self.text = text
        self.style = style
        self.type = type
        self.value = value
        self.confirm = confirm

    def as_dict(self):
        result = super().as_dict()
        result['confirm'] = self.confirm.as_dict() if self.confirm else self.confirm
        return result
