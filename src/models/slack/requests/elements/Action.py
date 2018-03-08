from marshmallow import Schema, fields, post_load

from src.models.slack.requests.elements.Option import OptionSchema


class Action:
    def __init__(self, name, selected_options=None):
        self.name = name
        self.selected_options = selected_options


class ActionSchema(Schema):
    name = fields.String(required=True)
    selected_options = fields.Nested(OptionSchema, many=True)

    @post_load
    def make_action(self, data):
        return Action(**data)

    class Meta:
        strict = True
