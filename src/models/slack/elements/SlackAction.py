from marshmallow import Schema, fields, post_load

from src.models.slack.elements.SlackOption import SlackOptionSchema


class SlackAction:
    def __init__(self, name, selected_options=None):
        self.name = name
        self.selected_options = selected_options


class SlackActionSchema(Schema):
    name = fields.String(required=True)
    selected_options = fields.Nested(SlackOptionSchema, many=True)

    @post_load
    def make_action(self, data):
        return SlackAction(**data)

    class Meta:
        strict = True
