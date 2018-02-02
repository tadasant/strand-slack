from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField

from src.domain.models.portal.SlackAgentStatus import SlackAgentStatus
from src.domain.models.portal.SlackApplicationInstallation import SlackApplicationInstallationSchema
from src.domain.models.portal.SlackTeam import SlackTeamSchema


class SlackAgent:
    def __init__(self, status, slack_team=None, slack_application_installation=None, discuss_channel_id=None):
        self.status = status
        self.discuss_channel_id = discuss_channel_id

        self.slack_team = slack_team
        self.slack_application_installation = slack_application_installation


class SlackAgentSchema(Schema):
    status = EnumField(SlackAgentStatus, required=True)
    discuss_channel_id = fields.String()
    slack_team = fields.Nested(SlackTeamSchema)
    slack_application_installation = fields.Nested(SlackApplicationInstallationSchema, allow_none=True)

    @post_load
    def make_slack_agent(self, data):
        return SlackAgent(**data)

    class Meta:
        strict = True
