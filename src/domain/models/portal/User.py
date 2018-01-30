from marshmallow import Schema, fields, post_load


class Tag:
    def __init__(self, name):
        self.name = name


class TagSchema(Schema):
    name = fields.String(required=True)

    @post_load
    def make_tag(self, data):
        return Tag(**data)

    class Meta:
        strict = True
