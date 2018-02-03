from marshmallow import Schema, fields, post_load

from src.domain.models.Model import Model


class File(Model):
    def __init__(self, id, public_url_shared=None, permalink_public=None):
        self.id = id
        self.public_url_shared = public_url_shared
        self.permalink_public = permalink_public


class FileSchema(Schema):
    id = fields.String(required=True)
    public_url_shared = fields.String()
    permalink_public = fields.String()

    @post_load
    def make_file(self, data):
        return File(**data)

    class Meta:
        strict = True
