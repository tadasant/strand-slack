class Message:
    def __init__(self, text, attachments=None):
        if attachments is None:
            attachments = []
        self.text = text
        self.attachments = attachments

    def as_dict(self):
        result = vars(self)
        result['attachments'] = [vars(attachment) for attachment in self.attachments]
        return result
