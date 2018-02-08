from http import HTTPStatus
from threading import Thread

from flask import request, current_app

from src.blueprints.slack.SlackResource import SlackResource
from src.domain.models.slack.requests.EventRequest import EventRequestSchema
from src.domain.repositories.SlackAgentRepository import slack_agent_repository
from src.service.type.TopicChannelMessageService import TopicChannelMessageService
from src.service.type.DiscussionMessageService import DiscussionMessageService


class EventResource(SlackResource):
    def post(self):
        """Receive events for which we are registered from Slack (Events API)"""
        result = ({}, HTTPStatus.OK)
        try:
            self.logger.info(f'Processing Event request: {request.get_json()}')
            payload = request.get_json()
            self._authenticate(payload)
            event_request = EventRequestSchema().load(payload).data
            if event_request.is_verification_request:
                result = ({'challenge': event_request.challenge}, HTTPStatus.OK)
            elif event_request.event and event_request.event.is_message_channels_event:
                if event_request.event.is_message and not event_request.event.hidden:
                    topic_channel_id = slack_agent_repository.get_topic_channel_id(
                        slack_team_id=event_request.team_id
                    )
                    if event_request.event.channel == topic_channel_id:
                        self.logger.info('Message in topic channel')
                        bot_user_id = slack_agent_repository.get_slack_bot_user_id(event_request.team_id)
                        service = TopicChannelMessageService(slack_client_wrapper=current_app.slack_client_wrapper,
                                                             portal_client_wrapper=current_app.portal_client_wrapper,
                                                             event_request=event_request,
                                                             bot_user_id=bot_user_id)
                        Thread(target=service.execute, daemon=True).start()

                    else:
                        # TODO [CCS-81] Check whether or not this is #discussions-X vs. other should happen here via db
                        self.logger.info('Message in non-topic channel')
                        service = DiscussionMessageService(slack_client_wrapper=current_app.slack_client_wrapper,
                                                           portal_client_wrapper=current_app.portal_client_wrapper,
                                                           event_request=event_request)
                        Thread(target=service.execute, daemon=True).start()
        finally:
            # Slack will keep re-sending if we don't respond 200 OK, even in exception case on our end
            return result
