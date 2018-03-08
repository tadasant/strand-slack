import json
from http import HTTPStatus
from threading import Thread

from flask import current_app, request

from src.blueprints.slack.SlackResource import SlackResource
from src.command.StartDiscussionCommand import StartDiscussionCommand
from src.command.UpdateTopicChannelCommand import UpdateTopicChannelCommand
from src.domain.models.exceptions.UnexpectedSlackException import UnexpectedSlackException
from src.domain.models.slack.requests.InteractiveComponentRequest import InteractiveComponentRequestSchema
from src.service.type.CloseDiscussionService import CloseDiscussionService
from src.service.type.PostNewTopicService import PostNewTopicService


class InteractiveComponentResource(SlackResource):
    def post(self):
        """Receive an interactive component (e.g. menu, dialog box) payload"""
        self.logger.info(f'Processing InteractiveComponent request: {request.__dict__}')
        payload = json.loads(request.form['payload'])
        self._authenticate(payload)
        interactive_component_request = InteractiveComponentRequestSchema().load(payload).data
        r = interactive_component_request
        if r.is_post_topic_dialog_submission:
            command = StartDiscussionCommand(slack_client_wrapper=current_app.slack_client_wrapper,
                                             core_api_client_wrapper=current_app.core_api_client_wrapper,
                                             slack_team_id=r.team.id,
                                             submission=r.submission,
                                             slack_user_id=r.user.id,
                                             slack_channel_id=r.channel.id)
            Thread(target=command.execute, daemon=True).start()
            return {}, HTTPStatus.OK
        else:
            message = f'Could not interpret slack request: {r}'
            self.logger.error(message)
            raise UnexpectedSlackException(message=message)
