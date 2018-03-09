import json
from http import HTTPStatus

from flask import request

from src.blueprints.slack.SlackResource import SlackResource
from src.models.exceptions.UnexpectedSlackException import UnexpectedSlackException
from src.models.slack.requests.SlackInteractiveComponentRequest import InteractiveComponentRequestSchema


class InteractiveComponentResource(SlackResource):
    def post(self):
        """Receive an interactive component (e.g. menu, dialog box) payload"""
        self.logger.info(f'Processing InteractiveComponent request: {request.__dict__}')
        payload = json.loads(request.form['payload'])
        self._authenticate(payload)
        interactive_component_request = InteractiveComponentRequestSchema().load(payload).data
        r = interactive_component_request
        if r.is_post_topic_dialog_submission:
            # commands = StartDiscussionCommand(slack_client_wrapper=current_app.slack_client_wrapper,
            #                                  core_api_client_wrapper=current_app.core_api_client_wrapper,
            #                                  slack_team_id=r.team.id,
            #                                  submission=r.submission,
            #                                  slack_user_id=r.user.id,
            #                                  slack_channel_id=r.channel.id)
            # Thread(target=commands.execute, daemon=True).start()
            return {}, HTTPStatus.OK
        else:
            message = f'Could not interpret slack request: {r}'
            self.logger.error(message)
            raise UnexpectedSlackException(message=message)
