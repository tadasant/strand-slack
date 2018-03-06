from src.command.Command import Command
from src.domain.models.exceptions.WrapperException import WrapperException
from src.domain.models.portal.SlackUser import SlackUserSchema
from src.domain.repositories.SlackAgentRepository import slack_agent_repository
from src.service.subservice.MessageTextFormatter import MessageTextFormatter
from src.command.model.message.message_models import SavedMessageAsTopicMessage


class SaveMessageAsTopicCommand(Command):
    def __init__(self, slack_client_wrapper, portal_client_wrapper, slack_team_id,
                 slack_channel_id, original_poster_slack_user_id, slack_message_ts):
        super().__init__(slack_client_wrapper=slack_client_wrapper, portal_client_wrapper=portal_client_wrapper,
                         slack_team_id=slack_team_id)
        self.slack_channel_id = slack_channel_id
        self.original_poster_slack_user_id = original_poster_slack_user_id
        self.slack_message_ts = slack_message_ts

    def execute(self):
        slack_message = self.slack_client_wrapper.get_channel_message_by_timestamp(slack_team_id=self.slack_team_id,
                                                                                   slack_channel_id=
                                                                                   self.slack_channel_id,
                                                                                   latest=self.slack_message_ts,
                                                                                   oldest=self.slack_message_ts)
        text_formatter = MessageTextFormatter(discussion_message=slack_message)
        slack_message.text = text_formatter.format_text()

        topic = self._create_topic(slack_user_id=self.original_poster_slack_user_id,
                                   slack_team_id=self.slack_team_id,
                                   title='New topic', description='N/A',
                                   tag_names=[])

        discussion = self.portal_client_wrapper.create_discussion(topic_id=topic.id)

        self.portal_client_wrapper.create_message(text=slack_message.text,
                                                  discussion_id=discussion.id,
                                                  author_id=topic.original_poster.id,
                                                  time=slack_message.time)

        self.portal_client_wrapper.close_discussion(discussion_id=discussion.id)

        topic_channel_id = slack_agent_repository.get_topic_channel_id(self.slack_team_id)
        self.slack_client_wrapper.send_ephemeral_message(slack_team_id=self.slack_team_id,
                                                         slack_channel_id=self.slack_channel_id,
                                                         slack_user_id=self.original_poster_slack_user_id,
                                                         text=SavedMessageAsTopicMessage(topic_channel_id).text)

    def _create_topic(self, slack_user_id, slack_team_id, title, description, tag_names):
        try:
            topic = self.portal_client_wrapper.create_topic_from_slack(
                title=title,
                description=description,
                original_poster_slack_user_id=slack_user_id,
                tag_names=tag_names
            )
        except WrapperException as e:
            if e.errors and e.errors[0]['message'] == 'SlackUser matching query does not exist':
                self.logger.info('Tried to create topic for unknown user. Retrying with user creation.')
                slack_user_info = self.slack_client_wrapper.get_user_info(slack_user_id=slack_user_id,
                                                                          slack_team_id=slack_team_id)
                slack_user = SlackUserSchema().load(slack_user_info).data
                topic = self.portal_client_wrapper.create_topic_and_user_as_original_poster_from_slack(
                    title=title,
                    description=description,
                    slack_user=slack_user,
                    tag_names=tag_names
                )
            else:
                raise e
        return topic
