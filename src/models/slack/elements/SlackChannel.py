from marshmallow import Schema, fields, post_load

from src.models.Model import Model


class SlackChannel(Model):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class SlackChannelSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)

    @post_load
    def make_channel(self, data):
        return SlackChannel(**data)

    class Meta:
        strict = True
