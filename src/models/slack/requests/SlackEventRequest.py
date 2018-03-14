import json
from copy import deepcopy

from marshmallow import Schema, fields, post_load

from src.models.Model import Model
from src.models.slack.elements.SlackEvent import SlackEventSchema, SlackEvent


class SlackEventRequest(Model):
    def __init__(self, type, token, challenge=None, team_id=None, event=None):
        self.type = type
        self.token = token
        self.challenge = challenge
        self.team_id = team_id
        self.event: SlackEvent = event

    @property
    def is_verification_request(self):
        return self.type == 'url_verification'

    def to_json(self):
        result = deepcopy(vars(self))
        result['event'] = json.loads(self.event.to_json())
        return json.dumps(result)


class SlackEventRequestSchema(Schema):
    type = fields.String(required=True)
    challenge = fields.String()
    team_id = fields.String()
    event = fields.Nested(SlackEventSchema)
    token = fields.String(required=True)

    @post_load
    def make_slack_event_request(self, data):
        return SlackEventRequest(**data)

    class Meta:
        strict = True
