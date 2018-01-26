import json

from flask import current_app, request
from flask_restful import Resource

from src.command.UpdateHelpChannelCommand import UpdateHelpChannelCommand
from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM

# TODO validate that this request is coming from Slack (payload['token'])
# TODO register errors (slack exceptions, wrapper exceptions, repository exceptions)
# TODO write tests
from src.common.logging import get_logger
from src.domain.models.exceptions.UnexpectedSlackException import UnexpectedSlackException
from src.domain.models.slack.InteractiveMenuResponse import InteractiveMenuResponseSchema


class InteractiveComponentResource(Resource):
    def __init__(self):
        super()
        self.logger = get_logger('InteractiveComponentResource')

    def post(self):
        """Receiving an interactive menu payload"""
        self.logger.info(f'Processing InteractiveComponent request: {request}')
        payload = json.loads(request.form['payload'])
        interactive_menu_response = InteractiveMenuResponseSchema().load(payload).data
        r = interactive_menu_response
        if r.type == 'interactive_message' and r.callback_id == INITIAL_ONBOARDING_DM.callback_id:
            help_channel_actions = [x for x in r.actions if x.name == INITIAL_ONBOARDING_DM.action_id]
            if len(help_channel_actions) != 1:
                message = f'Expected Slack call to have exactly (1) {INITIAL_ONBOARDING_DM.action_id} action'
                self.logger.error(message)
                raise UnexpectedSlackException(message=message)

            help_channel_selections = help_channel_actions[0].selected_options
            if len(help_channel_selections) != 1:
                message = f'Expected Slack call to have exactly (1) help channel selection'
                self.logger.error(message)
                raise UnexpectedSlackException(message=message)
            selected_channel_id = help_channel_selections[0].value

            UpdateHelpChannelCommand(slack_client_wrapper=current_app.slack_client_wrapper,
                                     portal_client_wrapper=current_app.portal_client_wrapper,
                                     slack_team_id=r.team.id,
                                     help_channel_id=selected_channel_id,
                                     response_url=r.response_url).execute()

        return None, 200
