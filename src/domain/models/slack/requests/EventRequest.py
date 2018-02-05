from marshmallow import Schema, fields, post_load

from src.domain.models.Model import Model
from src.domain.models.slack.requests.elements.Event import EventSchema


class EventRequest(Model):
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
    event = fields.Nested(EventSchema)

    @post_load
    def make_event_request(self, data):
        return EventRequest(**data)

    class Meta:
        strict = True
