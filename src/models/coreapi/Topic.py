from marshmallow import Schema, fields, post_load

from src.models.Model import Model
from src.models.coreapi.Tag import TagSchema
from src.models.coreapi.User import UserSchema


class Topic(Model):
    def __init__(self, id, title, description, tags, original_poster):
        self.id = id
        self.title = title
        self.description = description
        self.tags = tags
        self.original_poster = original_poster


class TopicSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    tags = fields.Nested(TagSchema, required=True, many=True)
    original_poster = fields.Nested(UserSchema, required=True)

    @post_load
    def make_topic(self, data):
        return Topic(**data)

    class Meta:
        strict = True
