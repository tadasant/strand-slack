from marshmallow import Schema, fields, post_load

from src.models.Model import Model


class SlackProfile(Model):
    def __init__(self, real_name, display_name, email):
        self.real_name = real_name
        self.display_name = display_name
        self.email = email


class SlackProfileSchema(Schema):
    real_name = fields.String(required=True)
    display_name = fields.String(required=True)
    email = fields.String(required=True)

    @post_load
    def make_slack_profile(self, data):
        return SlackProfile(**data)

    class Meta:
        strict = True
