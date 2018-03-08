from marshmallow import Schema, fields, post_load

from src.command.model.message.post_topic_dialog import POST_TOPIC_DIALOG
from src.domain.models.Model import Model
from src.domain.models.slack.Channel import ChannelSchema
from src.domain.models.slack.Team import TeamSchema
from src.domain.models.slack.User import UserSchema
from src.domain.models.slack.requests.elements.Action import ActionSchema
from src.domain.models.slack.requests.elements.Message import MessageSchema
from src.domain.models.slack.requests.elements.Submission import SubmissionSchema


class InteractiveComponentRequest(Model):
    def __init__(self, callback_id, team, user, channel, trigger_id=None, response_url=None, actions=None,
                 submission=None, original_message=None, type=None):
        self.type = type
        self.actions = actions
        self.callback_id = callback_id
        self.team = team
        self.original_message = original_message
        self.response_url = response_url
        self.submission = submission
        self.user = user
        self.channel = channel
        self.trigger_id = trigger_id

    @property
    def is_post_topic_dialog_submission(self):
        return self.type == 'dialog_submission' and self.callback_id == POST_TOPIC_DIALOG.callback_id


class InteractiveComponentRequestSchema(Schema):
    type = fields.String()
    actions = fields.Nested(ActionSchema, many=True)
    callback_id = fields.String(required=True)
    team = fields.Nested(TeamSchema, required=True)
    original_message = fields.Nested(MessageSchema)
    response_url = fields.String()
    submission = fields.Nested(SubmissionSchema)
    user = fields.Nested(UserSchema, required=True)
    trigger_id = fields.String()
    channel = fields.Nested(ChannelSchema, required=True)

    @post_load
    def make_interactive_component_request(self, data):
        return InteractiveComponentRequest(**data)

    class Meta:
        strict = True
