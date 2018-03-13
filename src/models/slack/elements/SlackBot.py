from marshmallow import Schema, fields, post_load

from src.models.Model import Model


class SlackBot(Model):
    def __init__(self, bot_user_id, bot_access_token):
        self.bot_user_id = bot_user_id
        self.bot_access_token = bot_access_token


class SlackBotSchema(Schema):
    bot_user_id = fields.String(required=True)
    bot_access_token = fields.String(required=True)

    @post_load
    def make_slack_bot(self, data):
        return SlackBot(**data)

    class Meta:
        strict = True
