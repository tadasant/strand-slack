from marshmallow import Schema, fields, post_load

from src.models.Model import Model


class SlackTeam(Model):
    def __init__(self, id):
        self.id = id


class SlackTeamSchema(Schema):
    id = fields.String(required=True)

    @post_load
    def make_team(self, data):
        return SlackTeam(**data)

    class Meta:
        strict = True
