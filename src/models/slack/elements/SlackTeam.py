from collections import namedtuple

from marshmallow import Schema, fields, post_load

SlackTeam = namedtuple(typename='Team', field_names='id')


class SlackTeamSchema(Schema):
    id = fields.String(required=True)

    @post_load
    def make_team(self, data):
        return SlackTeam(**data)

    class Meta:
        strict = True
