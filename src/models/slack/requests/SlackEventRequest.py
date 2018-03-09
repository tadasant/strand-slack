from marshmallow import Schema, fields, post_load

from src.models.Model import Model
from src.models.slack.elements.SlackEvent import SlackEventSchema


class SlackEventRequest(Model):
    def __init__(self, type, challenge=None, team_id=None, event=None):
        self.type = type
        self.challenge = challenge
        self.team_id = team_id
        self.event = event

    @property
    def is_verification_request(self):
        return self.type == 'url_verification'


class EventRequestSchema(Schema):
    type = fields.String(required=True)
    challenge = fields.String()
    team_id = fields.String()
    event = fields.Nested(SlackEventSchema)

    @post_load
    def make_event_request(self, data):
        return SlackEventRequest(**data)

    class Meta:
        strict = True
