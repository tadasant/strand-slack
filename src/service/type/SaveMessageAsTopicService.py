from threading import Thread

from src.domain.models.exceptions.WrapperException import WrapperException
from src.domain.models.portal.SlackUser import SlackUserSchema
from src.service.Service import Service


class SaveMessageAsTopicService(Service):
    """
        Creates topic for message
        Saves message as discussion
        Marks discussion as closed
    """

    def __init__(self, slack_client_wrapper, portal_client_wrapper, event_request):
        super().__init__(slack_client_wrapper=slack_client_wrapper, portal_client_wrapper=portal_client_wrapper)
        self.event_request = event_request

    def execute(self):
        message = self._get_original_message(slack_team_id=self.event_request.team_id,
                                             slack_channel_id=self.event_request.event.item.channel,
                                             latest=self.event_request.event.item.ts,
                                             oldest=self.event_request.event.item.ts)
        topic, user = self._create_topic()
        discussion = self._create_discussion()
        message = self._create_message()
        self._mark_discussion_as_closed()
        # getorcreateuser
        # create
        # createUserAndTopic
        # createDiscussion
        # createMessage
        # markDiscussionAsClosed
        pass

    def _get_original_message(self, slack_team_id, slack_channel_id, latest, oldest):
        message = self.slack_client_wrapper.get_channel_message_by_timestamp(slack_team_id=slack_team_id,
                                                                             slack_channel_id=slack_channel_id,
                                                                             latest=latest, oldest=oldest)
        return message

    def _create_topic(self):
        try:
            topic = self.portal_client_wrapper.create_topic_from_slack(
                title='New topic',
                description='NA',
                original_poster_slack_user_id=self.event_request.event.user,
                tag_names=[]
            )
        except WrapperException as e:
            if e.errors and e.errors[0]['message'] == 'SlackUser matching query does not exist':
                self.logger.info('Tried to create topic for unknown user. Retrying with user creation.')
                slack_user_info = self.slack_client_wrapper.get_user_info(slack_user_id=self.event_request.event.user,
                                                                          slack_team_id=self.event_request.team_id)
                slack_user = SlackUserSchema().load(slack_user_info).data
                topic = self.portal_client_wrapper.create_topic_and_user_as_original_poster_from_slack(
                    title='New topic',
                    description='NA',
                    slack_user=slack_user,
                    tag_names=[]
                )
            else:
                raise e
        return topic

    def _create_discussion(self):
        discussion = self.portal_client_wrapper.create_discussion()
        return discussion

    def _create_message(self):
        message = self.portal_client_wrapper.create_message()
        return message
