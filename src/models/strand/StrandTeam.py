from marshmallow import Schema, fields, post_load

from src.models.Model import Model


class StrandTeam(Model):
    def __init__(self, id):
        self.id = id


class StrandTeamSchema(Schema):
    id = fields.Integer(required=True)

    @post_load
    def make_strand_team(self, data):
        return StrandTeam(**data)

    class Meta:
        strict = True
