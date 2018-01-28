from marshmallow import Schema, fields, post_load

from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM
from src.domain.models.slack.Action import ActionSchema
from src.domain.models.slack.Message import MessageSchema
from src.domain.models.slack.Team import TeamSchema


class InteractiveMenuResponse:
    def __init__(self, type, actions, callback_id, team, original_message, response_url):
        self.type = type
        self.actions = actions
        self.callback_id = callback_id
        self.team = team
        self.original_message = original_message
        self.response_url = response_url

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
    def selected_help_channel_id(self):
        help_channel_actions = [x for x in self.actions if x.name == INITIAL_ONBOARDING_DM.action_id]
        help_channel_selections = help_channel_actions[0].selected_options
        return help_channel_selections[0].value


class InteractiveMenuResponseSchema(Schema):
    type = fields.String(required=True)
    actions = fields.Nested(ActionSchema, required=True, many=True)
    callback_id = fields.String(required=True)
    team = fields.Nested(TeamSchema, required=True)
    original_message = fields.Nested(MessageSchema, required=True)
    response_url = fields.String(required=True)

    @post_load
    def make_slack_team(self, data):
        return InteractiveMenuResponse(**data)
