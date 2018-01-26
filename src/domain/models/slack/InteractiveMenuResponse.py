from collections import namedtuple

from marshmallow import Schema, fields, post_load

from src.domain.models.slack.Action import ActionSchema
from src.domain.models.slack.Message import MessageSchema
from src.domain.models.slack.Team import TeamSchema

InteractiveMenuResponse = namedtuple(typename='InteractiveMenuResponse',
                                     field_names='type actions callback_id team original_message response_url')


class InteractiveMenuResponseSchema(Schema):
    type = fields.String(required=True)
    actions = fields.Nested(ActionSchema, required=True, many=True)
    callback_id = fields.String(required=True)
    team = fields.Nested(TeamSchema, required=True)
    original_message = fields.Nested(MessageSchema, required=True)
    response_url = fields.String(required=True)

    @post_load
    def make_slack_team(self, data):
        return InteractiveMenuResponse(**data)
