from marshmallow import Schema, fields, post_load

from src.models.Model import Model
from src.models.slack.elements.SlackBot import SlackBot


class SlackOauthAccessResponse(Model):
    def __init__(self, access_token, scope, team_name, team_id, bot, user_id):
        self.access_token = access_token
        self.scope = scope
        self.team_name = team_name
        self.team_id = team_id
        self.bot = bot
        self.user_id = user_id


class SlackOauthAccessResponseSchema(Schema):
    access_token = fields.String(required=True)
    scope = fields.String(required=True)
    team_name = fields.String(required=True)
    team_id = fields.String(required=True)
    bot = fields.Nested(SlackBot, required=True)
    user_id = fields.String(required=True)

    @post_load
    def make_slack_oauth_access_response(self, data):
        return SlackOauthAccessResponse(**data)

    class Meta:
        strict = True
