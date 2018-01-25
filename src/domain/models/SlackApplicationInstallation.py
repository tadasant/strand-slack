from marshmallow import Schema, fields, post_load

from src.domain.models import SlackTeamSchema
from src.domain.models import SlackUserSchema


class SlackApplicationInstallation:
    def __init__(self, access_token, bot_access_token, installer):
        self.access_token = access_token
        self.installer = installer
        self.bot_access_token = bot_access_token


class SlackApplicationInstallationSchema(Schema):
    slack_team = fields.Nested(SlackTeamSchema, required=True)
    access_token = fields.String(required=True)
    installer = fields.Nested(SlackUserSchema, required=True)
    bot_access_token = fields.String(required=True)

    @post_load
    def make_slack_application_installation(self, data):
        return SlackApplicationInstallation(**data)

    class Meta:
        strict = True
