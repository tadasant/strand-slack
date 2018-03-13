import json
from copy import deepcopy

from marshmallow import Schema, fields, post_load

from src.models.Model import Model
from src.models.slack.elements.SlackProfile import SlackProfileSchema


class SlackUser(Model):
    def __init__(self, id, profile=None):
        self.id = id
        self.profile = profile

    def to_json(self):
        result = deepcopy(vars(self))
        result['profile'] = json.loads(self.profile.to_json())
        return json.dumps(result)


class SlackUserSchema(Schema):
    id = fields.String(required=True)
    profile = fields.Nested(SlackProfileSchema)

    @post_load
    def make_slack_user(self, data):
        return SlackUser(**data)

    class Meta:
        strict = True
