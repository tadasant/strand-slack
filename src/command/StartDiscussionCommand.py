from src import slack_agent_repository
from src.command.Command import Command
from src.command.messages.formatted_text import discussion_initiation_message, discussion_initiation_dm
from src.domain.models.exceptions.WrapperException import WrapperException
from src.domain.models.portal.SlackUser import SlackUserSchema
from src.domain.models.slack.Channel import ChannelSchema
from src.domain.models.slack.Message import MessageSchema


class StartDiscussionCommand(Command):
    def __init__(self, slack_client_wrapper, portal_client_wrapper, slack_team_id, submission, slack_user_id):
        super().__init__(slack_team_id=slack_team_id, slack_client_wrapper=slack_client_wrapper,
                         portal_client_wrapper=portal_client_wrapper)
        self.submission = submission
        self.slack_user_id = slack_user_id

    def execute(self):
        self.logger.info(f'Executing StartDiscussionCommand for {self.slack_team_id}')
        try:
            topic = self._create_topic()
            slack_channel = self._create_channel(topic=topic)
            self.portal_client_wrapper.create_discussion(topic_id=topic.id, slack_channel=slack_channel,
                                                         slack_team_id=self.slack_team_id)
            self.slack_client_wrapper.invite_user_to_channel(slack_team_id=self.slack_team_id,
                                                             slack_channel_id=slack_channel.id,
                                                             slack_user_id=self.slack_user_id)
            self.slack_client_wrapper.send_message(slack_team_id=self.slack_team_id,
                                                   slack_channel_id=slack_channel.id,
                                                   text=discussion_initiation_message(
                                                       original_post_slack_user_id=self.slack_user_id,
                                                       title=self.submission.title,
                                                       description=self.submission.description,
                                                       tags=self.submission.tags
                                                   ))
            self._add_topic_to_discuss_channel(topic=topic, original_poster_id=self.slack_user_id)
            self.slack_client_wrapper.send_dm_to_user(slack_team_id=self.slack_team_id,
                                                      slack_user_id=self.slack_user_id,
                                                      text=discussion_initiation_dm(slack_channel_id=slack_channel.id))
        except WrapperException as e:
            self.logger.error(f'Starting discussion failed. Submission: {self.submission}. Error: {e}')
            self.slack_client_wrapper.send_dm_to_user(slack_team_id=self.slack_team_id,
                                                      slack_user_id=self.slack_user_id,
                                                      text='Sorry, starting your discussion failed for some reason'
                                                           ' :see_no_evil: Please contact support@solutionloft.com')

    def _create_topic(self):
        # TODO [CCS-60] move tag parsing to useful validation (maybe derived attr on Submission)
        tag_names = [x.strip() for x in self.submission.tags.split(',')]
        try:
            topic = self.portal_client_wrapper.create_topic(title=self.submission.title,
                                                            description=self.submission.description,
                                                            original_poster_slack_user_id=self.slack_user_id,
                                                            tag_names=tag_names)
        except WrapperException as e:
            # TODO [CCS-15] caching user info to avoid relying on error
            if 'SlackUser matching query does not exist.' not in e.errors:
                raise e
            self.logger.info('Tried to create topic for unknown user. Retrying with user creation.')
            slack_user_info = self.slack_client_wrapper.get_user_info(slack_user_id=self.slack_user_id,
                                                                      slack_team_id=self.slack_team_id)
            slack_user = SlackUserSchema().load(slack_user_info).data
            topic = self.portal_client_wrapper.create_topic_and_user_as_original_poster(
                title=self.submission.title,
                description=self.submission.description,
                slack_user=slack_user,
                tag_names=tag_names
            )
        return topic

    def _create_channel(self, topic):
        channel_name = f'discussion-{topic.id}'
        slack_channel_info = self.slack_client_wrapper.create_channel(slack_team_id=self.slack_team_id,
                                                                      channel_name=channel_name)
        return ChannelSchema().load(slack_channel_info).data

    def _add_topic_to_discuss_channel(self, topic, original_poster_id):
        discuss_channel_id = slack_agent_repository.get_discuss_channel_id(slack_team_id=self.slack_team_id)
        intro_message_info = self.slack_client_wrapper.get_last_channel_message(slack_team_id=self.slack_team_id,
                                                                                slack_channel_id=discuss_channel_id)
        intro_message = MessageSchema().load(intro_message_info).data
        # edit last message in channel to be the new question
        # re-add the intro message w/ message that the above discussion is new
        pass
