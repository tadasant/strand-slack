from marshmallow import Schema, fields, post_load

from src.models.Model import Model


class SlackSubmission(Model):
    def __init__(self, title, tags):
        self.title = title
        self.tags = tags


class SlackSubmissionSchema(Schema):
    title = fields.String(required=True)
    tags = fields.String(required=True)

    @post_load
    def make_slack_submission(self, data):
        return SlackSubmission(**data)

    class Meta:
        strict = True
