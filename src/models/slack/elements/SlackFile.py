from marshmallow import Schema, fields, post_load

from src.models.SlackModel import SlackModel


class SlackFile(SlackModel):
    def __init__(self, id, public_url_shared=None, permalink_public=None):
        self.id = id
        self.public_url_shared = public_url_shared
        self.permalink_public = permalink_public


class SlackFileSchema(Schema):
    id = fields.String(required=True)
    public_url_shared = fields.Boolean(allow_none=True)
    permalink_public = fields.String()

    @post_load
    def make_file(self, data):
        return SlackFile(**data)

    class Meta:
        strict = True
