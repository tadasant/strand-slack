from src.command.Command import Command
from src.command.messages.formatted_text import topic_channel_introduction
from src.domain.models.exceptions.WrapperException import WrapperException
from src.domain.repositories.SlackAgentRepository import slack_agent_repository


class UpdateTopicChannelCommand(Command):
    def __init__(self, slack_client_wrapper, portal_client_wrapper, slack_team_id, topic_channel_id, response_url):
        super().__init__(slack_client_wrapper=slack_client_wrapper, portal_client_wrapper=portal_client_wrapper,
                         slack_team_id=slack_team_id)
        self.topic_channel_id = topic_channel_id
        self.response_url = response_url

    def execute(self):
        """Set the #discuss channel setting and respond to the installer with success/failure"""
        log_message = f'Executing UpdateTopicChannel for {self.slack_team_id} with channel {self.topic_channel_id}'
        self.logger.info(log_message)
        response_payload = {
            'response_type': 'ephemeral',
            'replace_original': False,
        }
        try:
            messages = self.slack_client_wrapper.get_channel_messages(slack_team_id=self.slack_team_id,
                                                                      slack_channel_id=self.topic_channel_id)
            if len(messages) == 0:
                self.portal_client_wrapper.update_topic_channel_and_activate_agent(
                    slack_team_id=self.slack_team_id,
                    topic_channel_id=self.topic_channel_id)
                slack_bot_user_id = slack_agent_repository.get_slack_bot_user_id(slack_team_id=self.slack_team_id)
                self.slack_client_wrapper.invite_user_to_channel(slack_team_id=self.slack_team_id,
                                                                 slack_channel_id=self.topic_channel_id,
                                                                 slack_user_id=slack_bot_user_id)
                self.slack_client_wrapper.send_message(
                    slack_team_id=self.slack_team_id,
                    slack_channel_id=self.topic_channel_id,
                    text=topic_channel_introduction()
                )
                response_payload['text'] = f'Successfully set the topic channel to be <#{self.topic_channel_id}>.' \
                                           'If you want to change this later, just select a new option in the menu.'
            else:
                response_payload['text'] = f'Unable to set the channel to be <#{self.topic_channel_id}>.' \
                                           'You must select a newly-created, empty channel. Please try again.'
        except WrapperException as e:
            self.logger.error(f'Something went wrong! {e}')
            response_payload['text'] = 'Something went wrong! Please try again or contact support@solutionloft.com'
        self.slack_client_wrapper.post_to_response_url(response_url=self.response_url, payload=response_payload)
