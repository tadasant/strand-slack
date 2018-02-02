from marshmallow import Schema, fields, post_load

from src.domain.models.Model import Model


class Event(Model):
    def __init__(self, type, user, hidden=False, channel=None, text=None, ts=None, thread_ts=None):
        self.type = type
        self.user = user
        self.hidden = hidden
        self.channel = channel
        self.text = text
        self.ts = ts
        self.thread_ts = thread_ts

    @property
    def is_message_channels_event(self):
        if self.type == 'message':
            return self.channel and self.user and self.text and self.ts
        return False

    @property
    def is_message(self):
        return self.type == 'message'

    @property
    def is_reply(self):
        return self.is_message and self.thread_ts


class EventSchema(Schema):
    type = fields.String(required=True)
    user = fields.String(required=True)
    hidden = fields.Boolean()
    channel = fields.String()
    text = fields.String()
    ts = fields.String()
    thread_ts = fields.String()

    @post_load
    def make_event(self, data):
        return Event(**data)

    class Meta:
        strict = True
