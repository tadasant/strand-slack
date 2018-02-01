from src.command.Command import Command
from src.command.messages.formatted_text import discuss_introduction
from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM
from src.command.messages.update_discuss_channel_dm import UPDATE_DISCUSS_CHANNEL_DM
from src.domain.models.exceptions.WrapperException import WrapperException
from src.domain.repositories.SlackAgentRepository import slack_agent_repository


class UpdateDiscussChannelCommand(Command):
    def __init__(self, slack_client_wrapper, portal_client_wrapper, slack_team_id, discuss_channel_id, response_url):
        super().__init__(slack_client_wrapper=slack_client_wrapper, portal_client_wrapper=portal_client_wrapper,
                         slack_team_id=slack_team_id)
        self.discuss_channel_id = discuss_channel_id
        self.response_url = response_url

    def execute(self):
        log_message = f'Executing UpdateDiscussChannel for {self.slack_team_id} with channel {self.discuss_channel_id}'
        self.logger.info(log_message)
        response_payload = {
            'text': INITIAL_ONBOARDING_DM.text,
            'attachments': [UPDATE_DISCUSS_CHANNEL_DM.attachment_generator(discuss_channel_id=self.discuss_channel_id)]
        }
        try:
            self.portal_client_wrapper.update_discuss_channel_and_activate_agent(
                slack_team_id=self.slack_team_id,
                discuss_channel_id=self.discuss_channel_id)
            slack_bot_user_id = slack_agent_repository.get_slack_bot_user_id(slack_team_id=self.slack_team_id)
            self.slack_client_wrapper.invite_user_to_channel(slack_team_id=self.slack_team_id,
                                                             slack_channel_id=self.discuss_channel_id,
                                                             slack_user_id=slack_bot_user_id)
            self.slack_client_wrapper.send_message(
                slack_team_id=self.slack_team_id,
                slack_channel_id=self.discuss_channel_id,
                text=discuss_introduction()
            )
        except WrapperException:
            response_payload['attachments'] = [{'text': 'Something went wrong! Contact support@solutionloft.com'}]
        self.slack_client_wrapper.post_to_response_url(response_url=self.response_url, payload=response_payload)
