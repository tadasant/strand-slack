from collections import namedtuple

from marshmallow import Schema, fields, post_load

User = namedtuple(typename='User', field_names='id')


class UserSchema(Schema):
    id = fields.String(required=True)

    @post_load
    def make_user(self, data):
        return User(**data)
