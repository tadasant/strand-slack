import json
from copy import deepcopy

from marshmallow import Schema, fields, post_load

from src.models.Model import Model
from src.models.slack.elements.SlackEvent import SlackEventSchema, SlackEvent
from src.models.slack.elements.SlackUser import SlackUser


class SlackEventRequest(Model):
    def __init__(self, type, token, challenge=None, team_id=None, event=None, api_app_id=None, event_id=None,
                 event_time=None, authed_users=None):
        self.type = type
        self.token = token
        self.challenge = challenge
        self.team_id = team_id
        self.event: SlackEvent = event
        self.api_app_id = api_app_id
        self.event_id = event_id
        self.event_time = event_time
        self.authed_users = authed_users

    @property
    def is_verification_request(self):
        return self.type == 'url_verification'

    def to_json(self):
        result = deepcopy(vars(self))
        result['event'] = json.loads(self.event.to_json())
        result['authed_users'] = [json.loads(x.to_json()) for x in self.authed_users]
        return json.dumps(result)


class EventRequestSchema(Schema):
    type = fields.String(required=True)
    challenge = fields.String()
    team_id = fields.String()
    event = fields.Nested(SlackEventSchema)
    token = fields.String(required=True)
    api_app_id = fields.String()
    event_id = fields.String()
    event_time = fields.Integer()
    authed_users = fields.Nested(SlackUser, many=True)

    @post_load
    def make_event_request(self, data):
        return SlackEventRequest(**data)

    class Meta:
        strict = True
