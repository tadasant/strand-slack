from marshmallow import Schema, fields


class SlackTeamSchema(Schema):
    id = fields.Integer()
