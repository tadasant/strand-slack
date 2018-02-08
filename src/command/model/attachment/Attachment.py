from src.command.model.Model import Model


class Attachment(Model):
    def __init__(self, callback_id, color, attachment_type, actions, fallback=None):
        self.fallback = fallback
        self.callback_id = callback_id
        self.color = color
        self.attachment_type = attachment_type
        self.actions = actions

    def as_dict(self):
        result = super().as_dict()
        result['actions'] = [action.as_dict() for action in self.actions]
        return result
