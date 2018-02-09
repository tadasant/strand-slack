from src.command.model.Model import Model


class Action(Model):
    """Includes buttons"""

    def __init__(self, name, text, type, value, style=None, confirm=None):
        self.name = name
        self.text = text
        self.style = style
        self.type = type
        self.value = value
        if confirm:
            self.confirm = confirm

    def as_dict(self):
        result = super().as_dict()
        if 'confirm' in vars(self):
            result['confirm'] = self.confirm.as_dict()
        return result
