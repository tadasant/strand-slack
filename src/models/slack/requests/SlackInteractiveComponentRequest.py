from marshmallow import Schema, fields, post_load

from src.models.slack.responses.formats.dialogs import POST_TOPIC_DIALOG
from src.models.Model import Model
from src.models.slack.elements.SlackChannel import SlackChannelSchema
from src.models.slack.elements.SlackTeam import SlackTeamSchema
from src.models.slack.elements.SlackUser import SlackUserSchema
from src.models.slack.elements.SlackAction import SlackActionSchema
from src.models.slack.elements.SlackMessage import SlackMessageSchema
from src.models.slack.elements.SlackSubmission import SlackSubmissionSchema


class SlackInteractiveComponentRequest(Model):
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
    actions = fields.Nested(SlackActionSchema, many=True)
    callback_id = fields.String(required=True)
    team = fields.Nested(SlackTeamSchema, required=True)
    original_message = fields.Nested(SlackMessageSchema)
    response_url = fields.String()
    submission = fields.Nested(SlackSubmissionSchema)
    user = fields.Nested(SlackUserSchema, required=True)
    trigger_id = fields.String()
    channel = fields.Nested(SlackChannelSchema, required=True)

    @post_load
    def make_interactive_component_request(self, data):
        return SlackInteractiveComponentRequest(**data)

    class Meta:
        strict = True
