from src.commands.model.Model import Model


class Message(Model):
    def __init__(self, text, attachments=None):
        if attachments is None:
            attachments = []
        self.text = text
        self.attachments = attachments

    def as_dict(self):
        result = super().as_dict()
        result['attachments'] = [attachment.as_dict() for attachment in self.attachments]
        return result
