from marshmallow import Schema, fields, post_load


class EventItem:
    def __init__(self, type=None, channel=None, user=None, text=None, ts=None):
        self.type = type
        self.channel = channel
        self.user = user
        self.text = text
        self.ts = ts


class EventItemSchema(Schema):
    type = fields.String()
    channel = fields.String()
    user = fields.String()
    text = fields.String()
    ts = fields.String()

    @post_load
    def make_event_item(self, data):
        return EventItem(**data)

    class Meta:
        strict = True
