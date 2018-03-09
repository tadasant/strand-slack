class SlackAttachment:
    def __init__(self, fallback=None, color=None, author_name=None, fields=None, footer=None, footer_icon=None,
                 ts=None):
        self.fallback = fallback
        self.color = color
        self.author_name = author_name
        self.fields = fields
        self.footer = footer
        self.footer_icon = footer_icon
        self.ts = ts
