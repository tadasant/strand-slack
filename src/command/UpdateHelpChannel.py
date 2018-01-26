from src.command.messages.update_help_channel_dm import UPDATE_HELP_CHANNEL_DM
from src.common.logging import get_logger
from src.domain.models.exceptions.WrapperException import WrapperException


class UpdateHelpChannel:
    def __init__(self, slack_client_wrapper, portal_client_wrapper, slack_team_id, original_message_text,
                 help_channel_id, response_url):
        self.slack_client_wrapper = slack_client_wrapper
        self.portal_client_wrapper = portal_client_wrapper
        self.slack_team_id = slack_team_id
        self.original_message_text = original_message_text
        self.help_channel_id = help_channel_id
        self.response_url = response_url
        self.logger = get_logger('UpdateHelpChannel')

    def execute(self):
        self.logger.info(f'Executing UpdateHelpChannel for {self.team_id} with user {self.installer_id}')
        response_payload = {
            'text': self.original_message_text,
            'attachments': [UPDATE_HELP_CHANNEL_DM.attachment_generator(help_channel_id=self.help_channel_id)]
        }
        try:
            self.portal_client_wrapper.update_help_channel_and_activate_agent(
                slack_team_id=self.slack_team_id,
                help_channel_id=self.help_channel_id)
        except WrapperException:
            response_payload['attachments'] = [{'text': 'Something went wrong! Contact support@solutionloft.com'}]
        self.slack_client_wrapper.post_to_response_url(response_url=self.response_url, payload=response_payload)
