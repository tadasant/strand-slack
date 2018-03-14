from marshmallow import Schema, fields, post_load

from src.models.Model import Model


class SlackOption(Model):
    def __init__(self, value):
        self.value = value


class SlackOptionSchema(Schema):
    value = fields.String(required=True)

    @post_load
    def make_option(self, data):
        return SlackOption(**data)

    class Meta:
        strict = True
