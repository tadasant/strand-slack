from marshmallow import Schema, fields, post_load

from src.models.Model import Model


class SlackItem(Model):
    def __init__(self, type, channel=None, ts=None, file=None):
        self.type = type
        self.channel = channel
        self.ts = ts
        self.file = file


class SlackItemSchema(Schema):
    type = fields.String(required=True)
    channel = fields.String()
    ts = fields.String()
    file = fields.String()

    @post_load
    def make_item(self, data):
        return SlackItem(**data)

    class Meta:
        strict = True
