from marshmallow import Schema, fields


class SlackUserSchema(Schema):
    id = fields.Integer()
