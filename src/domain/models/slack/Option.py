from collections import namedtuple

from marshmallow import Schema, fields, post_load

Option = namedtuple(typename='Option', field_names='value')


class OptionSchema(Schema):
    value = fields.String(required=True)

    @post_load
    def make_option(self, data):
        return Option(**data)
