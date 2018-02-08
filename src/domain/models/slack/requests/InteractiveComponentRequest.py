from marshmallow import Schema, fields, post_load

from src.command.button.buttons import POST_NEW_TOPIC_BUTTON
from src.command.message.initial_onboarding_dm import INITIAL_ONBOARDING_DM
from src.command.message.post_topic_dialog import POST_TOPIC_DIALOG
from src.domain.models.Model import Model
from src.domain.models.slack.Team import TeamSchema
from src.domain.models.slack.User import UserSchema
from src.domain.models.slack.requests.elements.Action import ActionSchema
from src.domain.models.slack.requests.elements.Message import MessageSchema
from src.domain.models.slack.requests.elements.Submission import SubmissionSchema


class InteractiveComponentRequest(Model):
    def __init__(self, callback_id, team, user, trigger_id=None, response_url=None, actions=None, submission=None,
                 original_message=None, type=None):
        self.type = type
        self.actions = actions
        self.callback_id = callback_id
        self.team = team
        self.original_message = original_message
        self.response_url = response_url
        self.submission = submission
        self.user = user
        self.trigger_id = trigger_id

    @property
    def is_topic_channel_selection(self):
        if self.type == 'interactive_message' and self.callback_id == INITIAL_ONBOARDING_DM.callback_id:
            topic_channel_actions = [x for x in self.actions if x.name == INITIAL_ONBOARDING_DM.action_id]
            if len(topic_channel_actions) != 1:
                return False

            topic_channel_selections = topic_channel_actions[0].selected_options
            if len(topic_channel_selections) != 1:
                return False
        else:
            return False
        return True

    @property
    def is_post_topic_dialog_submission(self):
        return self.type == 'dialog_submission' and self.callback_id == POST_TOPIC_DIALOG.callback_id

    @property
    def is_post_new_topic_button_click(self):
        return self.callback_id == POST_NEW_TOPIC_BUTTON.callback_id

    @property
    def selected_topic_channel_id(self):
        topic_channel_actions = [x for x in self.actions if x.name == INITIAL_ONBOARDING_DM.action_id]
        topic_channel_selections = topic_channel_actions[0].selected_options
        return topic_channel_selections[0].value


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

    @post_load
    def make_interactive_component_request(self, data):
        return InteractiveComponentRequest(**data)

    class Meta:
        strict = True
