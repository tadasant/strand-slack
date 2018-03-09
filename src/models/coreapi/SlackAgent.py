from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField

from src.models.SlackModel import SlackModel
from src.models.coreapi.SlackAgentStatus import SlackAgentStatus
from src.models.coreapi.SlackApplicationInstallation import SlackApplicationInstallationSchema
from src.models.coreapi.SlackTeam import SlackTeamSchema


class SlackAgent(SlackModel):
    def __init__(self, status, slack_team=None, slack_application_installation=None, topic_channel_id=None):
        self.status = status
        self.topic_channel_id = topic_channel_id

        self.slack_team = slack_team
        self.slack_application_installation = slack_application_installation


class SlackAgentSchema(Schema):
    status = EnumField(SlackAgentStatus, required=True)
    topic_channel_id = fields.String(allow_none=True)
    slack_team = fields.Nested(SlackTeamSchema)
    slack_application_installation = fields.Nested(SlackApplicationInstallationSchema, allow_none=True)

    @post_load
    def make_slack_agent(self, data):
        return SlackAgent(**data)

    class Meta:
        strict = True
