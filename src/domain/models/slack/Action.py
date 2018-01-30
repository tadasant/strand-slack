from collections import namedtuple

from marshmallow import Schema, fields, post_load

from src.domain.models.slack.Option import OptionSchema

Action = namedtuple(typename='Action', field_names='name selected_options')


class ActionSchema(Schema):
    name = fields.String(required=True)
    selected_options = fields.Nested(OptionSchema, required=True, many=True)

    @post_load
    def make_action(self, data):
        return Action(**data)

    class Meta:
        strict = True
