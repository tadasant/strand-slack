from marshmallow import Schema, fields, post_load

from src.domain.models.Model import Model


class Item(Model):
    def __init__(self, type, channel=None, ts=None, file=None):
        self.type = type
        self.channel = channel
        self.ts = ts
        self.file = file


class ItemSchema(Schema):
    type = fields.String(required=True)
    channel = fields.String()
    ts = fields.String()
    file = fields.String()

    @post_load
    def make_item(self, data):
        return Item(**data)

    class Meta:
        strict = True
