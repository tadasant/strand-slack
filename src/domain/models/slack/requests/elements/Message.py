from collections import namedtuple

from marshmallow import Schema, fields, post_load

Message = namedtuple(typename='Message', field_names='text ts')


class MessageSchema(Schema):
    text = fields.String(required=True)
    ts = fields.String(required=True)

    @post_load
    def make_message(self, data):
        return Message(**data)

    class Meta:
        strict = True
