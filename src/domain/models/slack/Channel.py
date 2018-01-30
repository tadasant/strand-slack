from collections import namedtuple

from marshmallow import Schema, fields, post_load

Channel = namedtuple(typename='Channel', field_names='id name')


class ChannelSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)

    @post_load
    def make_channel(self, data):
        return Channel(**data)
