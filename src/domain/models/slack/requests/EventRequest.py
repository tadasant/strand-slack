from marshmallow import Schema, fields, post_load

from src.domain.models.slack.requests.elements.Event import EventSchema


class EventRequest:
    def __init__(self, team_id, event):
        self.team_id = team_id
        self.event = event


class EventRequestSchema(Schema):
    team_id = fields.String(required=True)
    event = fields.Nested(EventSchema, required=True)

    @post_load
    def make_event_request(self, data):
        return EventRequest(**data)

    class Meta:
        strict = True
