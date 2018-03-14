from marshmallow import Schema, fields, post_load

from src.models.Model import Model


class StrandStrand(Model):
    def __init__(self, id):
        self.id = id


class StrandStrandSchema(Schema):
    id = fields.Integer(required=True)

    @post_load
    def make_strand_strand(self, data):
        return StrandStrand(**data)

    class Meta:
        strict = True
