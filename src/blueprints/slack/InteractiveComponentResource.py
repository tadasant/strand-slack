import json
from http import HTTPStatus
from threading import Thread

from flask import current_app, request

from src.blueprints.slack.SlackResource import SlackResource
from src.command.UpdateHelpChannelCommand import UpdateHelpChannelCommand
from src.domain.models.exceptions.UnexpectedSlackException import UnexpectedSlackException
from src.domain.models.slack.InteractiveMenuRequest import InteractiveMenuRequestSchema


class InteractiveComponentResource(SlackResource):
    def post(self):
        """Receiving an interactive menu payload"""
        self.logger.info(f'Processing InteractiveComponent request: {request}')
        payload = json.loads(request.form['payload'])
        self._authenticate(payload)
        interactive_menu_response = InteractiveMenuRequestSchema().load(payload).data
        r = interactive_menu_response
        if r.is_help_channel_selection:
            command = UpdateHelpChannelCommand(slack_client_wrapper=current_app.slack_client_wrapper,
                                               portal_client_wrapper=current_app.portal_client_wrapper,
                                               slack_team_id=r.team.id,
                                               help_channel_id=r.selected_help_channel_id,
                                               response_url=r.response_url)
            Thread(target=command.execute).start()
        else:
            message = f'Could not interpret slack request: {r}'
            self.logger.error(message)
            raise UnexpectedSlackException(message=message)

        return '', HTTPStatus.NO_CONTENT
