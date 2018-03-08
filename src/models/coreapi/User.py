from marshmallow import Schema, fields, post_load

from src.models.Model import Model


class User(Model):
    def __init__(self, id):
        self.id = id


class UserSchema(Schema):
    id = fields.Integer(required=True)

    @post_load
    def make_user(self, data):
        return User(**data)

    class Meta:
        strict = True
