from collections import namedtuple

from marshmallow import Schema, fields, post_load

# These fields are from the 'name' fields on our only dialog: POST_TOPIC_DIALOG
Submission = namedtuple(typename='Submission', field_names='title description tags')


class SubmissionSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    tags = fields.String(required=True)

    def __repr__(self):
        return f'<{self.__class__}({self.__dict__})>'

    @post_load
    def make_submission(self, data):
        return Submission(**data)

    class Meta:
        strict = True
