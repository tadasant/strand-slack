from marshmallow import Schema, fields, post_load

from src.domain.models.Model import Model
from src.domain.models.slack.requests.elements.EventItem import EventItemSchema


class Event(Model):
    def __init__(self, type, user, item):
        self.type = type
        self.user = user
        self.item = item

    @property
    def is_message_channels_event(self):
        if self.item.type == 'message':
            return self.item.channel and self.item.user and self.item.text and self.item.ts
        return False


class EventSchema(Schema):
    type = fields.String(required=True)
    user = fields.String(required=True)
    item = fields.Nested(EventItemSchema, required=True)

    @post_load
    def make_event(self, data):
        return Event(**data)

    class Meta:
        strict = True
