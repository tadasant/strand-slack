from marshmallow import Schema, fields, post_load

from src.domain.models.portal.User import TagSchema


class Topic:
    def __init__(self, id, title, description, tags):
        self.id = id
        self.title = title
        self.description = description
        self.tags = tags


class TopicSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    tags = fields.Nested(TagSchema, required=True, many=True)

    @post_load
    def make_topic(self, data):
        return Topic(**data)

    class Meta:
        strict = True
