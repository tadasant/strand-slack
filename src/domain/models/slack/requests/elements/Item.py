from marshmallow import Schema, fields, post_load

from src.domain.models.Model import Model


class Item(Model):
    def __init__(self, type, channel, ts):
        self.type = type
        self.channel = channel
        self.ts = ts


class ItemSchema(Schema):
    type = fields.String(required=True)
    channel = fields.String(required=True)
    ts = fields.String(required=True)

    @post_load
    def make_file(self, data):
        return Item(**data)

    class Meta:
        strict = True
