from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField

from src.domain.models.portal.SlackAgentStatus import SlackAgentStatus
from src.domain.models.portal.SlackApplicationInstallation import SlackApplicationInstallationSchema
from src.domain.models.portal.SlackTeam import SlackTeamSchema


class SlackAgent:
    def __init__(self, status, slack_team, slack_application_installation, help_channel_id=None):
        self.status = status
        self.help_channel_id = help_channel_id

        self.slack_team = slack_team
        self.slack_application_installation = slack_application_installation


class SlackAgentSchema(Schema):
    status = EnumField(SlackAgentStatus, required=True)
    help_channel_id = fields.String(allow_none=True)
    slack_team = fields.Nested(SlackTeamSchema, required=True)
    slack_application_installation = fields.Nested(SlackApplicationInstallationSchema)

    @post_load
    def make_slack_agent(self, data):
        return SlackAgent(**data)

    class Meta:
        strict = True
