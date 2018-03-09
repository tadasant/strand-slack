from collections import namedtuple

from marshmallow import Schema, fields, post_load

SlackUser = namedtuple(typename='User', field_names='id')


class SlackUserSchema(Schema):
    id = fields.String(required=True)

    @post_load
    def make_user(self, data):
        return SlackUser(**data)

    class Meta:
        strict = True
