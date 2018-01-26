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
        if r.is_help_channel_selection():
            # TODO CCS-38 multithread commands -- should respond to Slack immediately
            response = UpdateHelpChannelCommand(slack_client_wrapper=current_app.slack_client_wrapper,
                                                portal_client_wrapper=current_app.portal_client_wrapper,
                                                slack_team_id=r.team.id,
                                                help_channel_id=r.get_selected_help_channel_id(),
                                                response_url=r.response_url).execute()
        else:
            message = f'Could not interpret slack request: {r}'
            self.logger.error(message)
            return f'Error: {message}', 400

        return response, 200
