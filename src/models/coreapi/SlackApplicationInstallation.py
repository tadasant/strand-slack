from marshmallow import Schema, fields, post_load

from src.models.SlackModel import SlackModel
from src.models.coreapi.SlackUser import SlackUserSchema


class SlackApplicationInstallation(SlackModel):
    def __init__(self, access_token, bot_access_token, installer, bot_user_id):
        self.access_token = access_token
        self.installer = installer
        self.bot_access_token = bot_access_token
        self.bot_user_id = bot_user_id


class SlackApplicationInstallationSchema(Schema):
    access_token = fields.String(required=True)
    installer = fields.Nested(SlackUserSchema, required=True)
    bot_access_token = fields.String(required=True)
    bot_user_id = fields.String(required=True)

    @post_load
    def make_slack_application_installation(self, data):
        return SlackApplicationInstallation(**data)

    class Meta:
        strict = True
