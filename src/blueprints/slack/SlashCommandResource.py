from http import HTTPStatus
from threading import Thread

from flask import current_app, request

from src.blueprints.slack.SlackResource import SlackResource
from src.domain.models.exceptions.UnexpectedSlackException import UnexpectedSlackException
from src.domain.models.slack.requests.SlashCommandRequest import SlashCommandRequestSchema
from src.service.type.CloseDiscussionService import CloseDiscussionService
from src.service.type.PostNewTopicService import PostNewTopicService


class SlashCommandResource(SlackResource):
    def post(self):
        """Receive a slash command for which we are registered"""
        self.logger.info(f'Processing SlashCommand request: {request}')
        payload = request.form
        self._authenticate(payload)
        slash_command_request = SlashCommandRequestSchema().load(payload).data
        r = slash_command_request
        if r.is_post_topic:
            service = PostNewTopicService(slack_client_wrapper=current_app.slack_client_wrapper,
                                          trigger_id=r.trigger_id,
                                          slack_team_id=r.team_id,
                                          slack_user_id=r.user_id)
            Thread(target=service.execute, daemon=True).start()
        elif r.is_close_discussion:
            # TODO [CCS-81] Authenticating user is OP/admin should happen here via DB
            service = CloseDiscussionService(slack_client_wrapper=current_app.slack_client_wrapper,
                                             portal_client_wrapper=current_app.portal_client_wrapper,
                                             slack_team_id=r.team_id,
                                             slack_user_id=r.user_id,
                                             slack_channel_id=r.channel_id)
            Thread(target=service.execute, daemon=True).start()
        else:
            message = f'Could not interpret slack request: {r}'
            self.logger.error(message)
            raise UnexpectedSlackException(message=message)

        return '', HTTPStatus.NO_CONTENT
