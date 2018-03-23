from marshmallow import Schema, fields, post_load

from src.models.Model import Model


class SlackTokens(Model):
    def __init__(self, oauth=None, bot=None):
        if oauth:
            self.oauth = oauth
        if bot:
            self.bot = bot


class SlackTokensSchema(Schema):
    oauth = fields.List(fields.String(), allow_none=True)
    bot = fields.List(fields.String(), allow_none=True)

    @post_load
    def make_slack_token(self, data):
        return SlackTokens(**data)

    class Meta:
        strict = True
