from collections import namedtuple

from marshmallow import Schema, fields, post_load

Team = namedtuple(typename='Team', field_names='id')


class TeamSchema(Schema):
    id = fields.String(required=True)

    @post_load
    def make_team(self, data):
        return Team(**data)

    class Meta:
        strict = True
