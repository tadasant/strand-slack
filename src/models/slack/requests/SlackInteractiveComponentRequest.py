import json
from copy import deepcopy

from marshmallow import Schema, fields, post_load

from src.models.Model import Model
from src.models.slack.elements.SlackAction import SlackActionSchema
from src.models.slack.elements.SlackChannel import SlackChannelSchema
from src.models.slack.elements.SlackMessage import SlackMessageSchema
from src.models.slack.elements.SlackSubmission import SlackSubmissionSchema
from src.models.slack.elements.SlackTeam import SlackTeamSchema
from src.models.slack.elements.SlackUser import SlackUserSchema
from src.models.slack.outgoing.actions import EditMetadataButton
from src.models.slack.outgoing.dialogs import EditMetadataDialog


class SlackInteractiveComponentRequest(Model):
    def __init__(self, callback_id, team, user, channel, token, trigger_id=None, response_url=None, actions=None,
                 submission=None, original_message=None, type=None):
        self.type = type
        self.token = token
        self.actions = actions
        self.callback_id = callback_id
        self.team = team
        self.original_message = original_message
        self.response_url = response_url
        self.submission = submission
        self.user = user
        self.channel = channel
        self.trigger_id = trigger_id

    def to_json(self):
        result = deepcopy(vars(self))
        result['actions'] = [json.loads(x.to_json()) for x in self.actions] if self.actions else None
        result['team'] = json.loads(self.team.to_json()) if self.team else None
        result['original_message'] = json.loads(self.original_message.to_json()) if self.original_message else None
        result['submission'] = json.loads(self.submission.to_json()) if self.submission else None
        result['user'] = json.loads(self.user.to_json()) if self.user else None
        result['channel'] = json.loads(self.channel.to_json()) if self.channel else None
        return json.dumps(result)

    @property
    def is_edit_metadata_dialog_submission(self):
        callback_id_prefix = self.callback_id.split('-')[0]
        return self.type == 'dialog_submission' and callback_id_prefix == EditMetadataDialog.callback_id_prefix

    @property
    def is_edit_metadata_button(self):
        return self.actions and self.actions[0].name == EditMetadataButton().name


class InteractiveComponentRequestSchema(Schema):
    type = fields.String()
    token = fields.String(required=True)
    actions = fields.Nested(SlackActionSchema, many=True)
    callback_id = fields.String(required=True)
    team = fields.Nested(SlackTeamSchema, required=True)
    original_message = fields.Nested(SlackMessageSchema, allow_none=True)
    response_url = fields.String()
    submission = fields.Nested(SlackSubmissionSchema, allow_none=True)
    user = fields.Nested(SlackUserSchema, required=True)
    trigger_id = fields.String()
    channel = fields.Nested(SlackChannelSchema, required=True)

    @post_load
    def make_interactive_component_request(self, data):
        return SlackInteractiveComponentRequest(**data)

    class Meta:
        strict = True
