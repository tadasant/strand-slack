from marshmallow import Schema, fields, post_load

from src.models.SlackTeam import SlackTeamSchema
from src.models.SlackUser import SlackUserSchema


class SlackApplicationInstallation:
    def __init__(self, slack_team, access_token, bot_access_token, installer=None, is_active=False):
        self.slack_team = slack_team
        self.access_token = access_token
        self.installer = installer
        self.bot_access_token = bot_access_token
        self.is_active = is_active


class SlackApplicationInstallationSchema(Schema):
    slack_team = fields.Nested(SlackTeamSchema, required=True)
    access_token = fields.String(required=True)
    installer = fields.Nested(SlackUserSchema)
    bot_access_token = fields.String(required=True)
    is_active = fields.Boolean(default=False)

    @post_load
    def make_slack_application_installation(self, data):
        return SlackApplicationInstallation(**data)

    class Meta:
        strict = True
