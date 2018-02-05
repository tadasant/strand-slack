from marshmallow import Schema, fields, post_load

from src.domain.models.Model import Model


class SlackProfile(Model):
    def __init__(self, image_72, first_name=None, last_name=None, display_name=None, email=None):
        self.image_72 = image_72
        self.first_name = first_name
        self.last_name = last_name
        self.display_name = display_name
        self.email = email


class SlackProfileSchema(Schema):
    image_72 = fields.String(required=True)
    first_name = fields.String()
    last_name = fields.String()
    display_name = fields.String()
    email = fields.String()

    @post_load
    def make_slack_profile(self, data):
        return SlackProfile(**data)
