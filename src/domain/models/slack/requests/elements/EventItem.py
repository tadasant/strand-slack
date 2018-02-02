from marshmallow import Schema, fields, post_load

from src.domain.models.Model import Model


class EventItem(Model):
    def __init__(self, type=None, hidden=False, channel=None, user=None, text=None, ts=None, thread_ts=None):
        self.type = type
        self.hidden = hidden
        self.channel = channel
        self.user = user
        self.text = text
        self.ts = ts
        self.thread_ts = thread_ts

    @property
    def is_message(self):
        return self.type == 'message'

    @property
    def is_reply(self):
        return self.is_message and self.thread_ts


class EventItemSchema(Schema):
    type = fields.String()
    hidden = fields.Boolean()
    channel = fields.String()
    user = fields.String()
    text = fields.String()
    ts = fields.String()
    thread_ts = fields.String()

    @post_load
    def make_event_item(self, data):
        return EventItem(**data)

    class Meta:
        strict = True
