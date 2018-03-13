from marshmallow import Schema, fields, post_load

from src.models.Model import Model


class StrandUser(Model):
    def __init__(self, id):
        self.id = id


class StrandUserSchema(Schema):
    id = fields.Integer(required=True)

    @post_load
    def make_strand_user(self, data):
        return StrandUser(**data)

    class Meta:
        strict = True
