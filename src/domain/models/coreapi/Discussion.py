from enum import Enum

from marshmallow import Schema, fields, post_load

from src.domain.models.Model import Model


class DiscussionStatus(Enum):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'


class Discussion(Model):
    def __init__(self, id):
        self.id = id


class DiscussionSchema(Schema):
    id = fields.Integer(required=True)

    @post_load
    def make_discussion(self, data):
        return Discussion(**data)

    class Meta:
        strict = True
