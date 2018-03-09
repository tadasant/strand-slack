from marshmallow import Schema, fields, post_load

from src.models.SlackModel import SlackModel


class Tag(SlackModel):
    def __init__(self, name):
        self.name = name


class TagSchema(Schema):
    name = fields.String(required=True)

    @post_load
    def make_tag(self, data):
        return Tag(**data)

    class Meta:
        strict = True
