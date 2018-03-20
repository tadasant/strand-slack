import json
from copy import deepcopy
from typing import List

from marshmallow import Schema, fields, post_load

from src.models.Model import Model
from src.models.slack.elements import SlackOption
from src.models.slack.elements.SlackOption import SlackOptionSchema


class SlackAction(Model):
    def __init__(self, name=None, text=None, type=None, value=None, style=None, confirm=None, selected_options=None):
        self.name = name
        self.text = text
        self.type = type
        self.value = value
        if style:
            self.style = style
        if confirm:
            self.confirm = confirm
        if selected_options:
            self.selected_options: List[SlackOption] = selected_options

    def to_json(self):
        result = deepcopy(vars(self))
        if hasattr(self, 'selected_options'):
            result['selected_options'] = [json.loads(x.to_json()) for x in
                                          self.selected_options] if self.selected_options else []
        return json.dumps(result)


class SlackActionSchema(Schema):
    name = fields.String(required=True)
    type = fields.String()
    value = fields.String()
    selected_options = fields.Nested(SlackOptionSchema, many=True)

    @post_load
    def make_action(self, data):
        return SlackAction(**data)

    class Meta:
        strict = True
