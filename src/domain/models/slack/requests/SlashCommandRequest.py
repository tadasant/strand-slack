from marshmallow import Schema, fields, post_load

from src.domain.models.Model import Model


class SlashCommandRequest(Model):
    def __init__(self, team_id, user_id, command, response_url, trigger_id, channel_id, text=None):
        self.team_id = team_id
        self.user_id = user_id
        self.command = command
        self.text = text
        self.response_url = response_url
        self.trigger_id = trigger_id
        self.channel_id = channel_id

    @property
    def is_post_topic(self):
        return self.command == '/codeclippy' and (self.text == 'post' or self.text == '')

    @property
    def is_close_discussion(self):
        return self.command == '/codeclippy' and self.text == 'close'


class SlashCommandRequestSchema(Schema):
    team_id = fields.String(required=True)
    user_id = fields.String(required=True)
    command = fields.String(required=True)
    text = fields.String()
    response_url = fields.String(required=True)
    trigger_id = fields.String(required=True)
    channel_id = fields.String(required=True)

    @post_load
    def make_slash_command_request(self, data):
        return SlashCommandRequest(**data)

    class Meta:
        strict = True
