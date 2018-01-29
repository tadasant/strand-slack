from marshmallow import Schema, fields, post_load


class SlashCommandRequest:
    def __init__(self, team_id, user_id, command, text, response_url):
        self.team_id = team_id
        self.user_id = user_id
        self.command = command
        self.text = text
        self.response_url = response_url

    @property
    def is_question_initiation(self):
        return self.command == '/ask'


class SlashCommandRequestSchema(Schema):
    team_id = fields.String(required=True)
    user_id = fields.String(required=True)
    command = fields.String(required=True)
    text = fields.String()
    response_url = fields.String(required=True)

    @post_load
    def make_slash_command_request(self, data):
        return SlashCommandRequest(**data)
