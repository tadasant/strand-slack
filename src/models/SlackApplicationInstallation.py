from collections import namedtuple

from marshmallow import Schema, fields

from src.models.SlackTeam import SlackTeamSchema
from src.models.SlackUser import SlackUserSchema

SlackApplicationInstallation = namedtuple(typename='SlackApplicationInstallation',
                                          field_names='slack_team access_token installer bot_access_token is_active')


class SlackApplicationInstallationSchema(Schema):
    slack_team = fields.Nested(SlackTeamSchema)
    access_token = fields.String()
    installer = fields.Nested(SlackUserSchema)
    bot_access_token = fields.String()
    is_active = fields.Boolean()

    class Meta:
        strict = True
