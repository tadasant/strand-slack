from marshmallow import Schema, fields, post_load

from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM
from src.command.messages.post_topic_dialog import POST_TOPIC_DIALOG
from src.domain.models.slack.Action import ActionSchema
from src.domain.models.slack.Message import MessageSchema
from src.domain.models.slack.Submission import SubmissionSchema
from src.domain.models.slack.Team import TeamSchema
from src.domain.models.slack.User import UserSchema


class InteractiveComponentRequest:
    def __init__(self, type, callback_id, team, user, response_url=None, actions=None, submission=None,
                 original_message=None):
        self.type = type
        self.actions = actions
        self.callback_id = callback_id
        self.team = team
        self.original_message = original_message
        self.response_url = response_url
        self.submission = submission
        self.user = user

    @property
    def is_help_channel_selection(self):
        if self.type == 'interactive_message' and self.callback_id == INITIAL_ONBOARDING_DM.callback_id:
            help_channel_actions = [x for x in self.actions if x.name == INITIAL_ONBOARDING_DM.action_id]
            if len(help_channel_actions) != 1:
                return False

            help_channel_selections = help_channel_actions[0].selected_options
            if len(help_channel_selections) != 1:
                return False
        else:
            return False
        return True

    @property
    def is_post_topic_dialog_submission(self):
        return self.type == 'dialog_submission' and self.callback_id == POST_TOPIC_DIALOG.callback_id

    @property
    def selected_help_channel_id(self):
        help_channel_actions = [x for x in self.actions if x.name == INITIAL_ONBOARDING_DM.action_id]
        help_channel_selections = help_channel_actions[0].selected_options
        return help_channel_selections[0].value


class InteractiveComponentRequestSchema(Schema):
    type = fields.String(required=True)
    actions = fields.Nested(ActionSchema, many=True)
    callback_id = fields.String(required=True)
    team = fields.Nested(TeamSchema, required=True)
    original_message = fields.Nested(MessageSchema)
    response_url = fields.String()
    submission = fields.Nested(SubmissionSchema)
    user = fields.Nested(UserSchema, required=True)

    @post_load
    def make_interactive_component_request(self, data):
        return InteractiveComponentRequest(**data)

    class Meta:
        strict = True
