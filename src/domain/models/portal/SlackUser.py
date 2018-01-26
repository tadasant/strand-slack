from collections import namedtuple

from marshmallow import Schema, fields, post_load

SlackUser = namedtuple(typename='SlackUser', field_names='id')


class SlackUserSchema(Schema):
    id = fields.String(required=True)

    @post_load
    def make_slack_team(self, data):
        return SlackUser(**data)
