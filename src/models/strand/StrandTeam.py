from marshmallow import Schema, fields, post_load

from src.models.Model import Model
from src.models.strand.StrandUser import StrandUserSchema


class StrandTeam(Model):
    def __init__(self, id=None, members=None):
        self.id = id
        self.members = members


class StrandTeamSchema(Schema):
    id = fields.Integer()
    members = fields.Nested(StrandUserSchema, many=True)

    @post_load
    def make_strand_team(self, data):
        return StrandTeam(**data)

    class Meta:
        strict = True
