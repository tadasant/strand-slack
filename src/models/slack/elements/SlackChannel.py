from collections import namedtuple

from marshmallow import Schema, fields, post_load

SlackChannel = namedtuple(typename='Channel', field_names='id name')


class SlackChannelSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)

    @post_load
    def make_channel(self, data):
        return SlackChannel(**data)

    class Meta:
        strict = True
