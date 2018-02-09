from src.command.model.Model import Model


class Confirm(Model):
    def __init__(self, title, text, ok_text, dismiss_text):
        self.title = title
        self.text = text
        self.ok_text = ok_text
        self.dismiss_text = dismiss_text
