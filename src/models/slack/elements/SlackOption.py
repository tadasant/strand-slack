from collections import namedtuple

from marshmallow import Schema, fields, post_load

SlackOption = namedtuple(typename='Option', field_names='value')


class SlackOptionSchema(Schema):
    value = fields.String(required=True)

    @post_load
    def make_option(self, data):
        return SlackOption(**data)

    class Meta:
        strict = True
