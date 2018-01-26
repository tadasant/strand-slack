from src.command.messages.onboarding_dm import ONBOARDING_DM
from src.common.logging import get_logger


class UpdateHelpChannel:
    def __init__(self, slack_client_wrapper, team_id, installer_id):
        self.slack_client_wrapper = slack_client_wrapper
        self.team_id = team_id
        self.installer_id = installer_id
        self.logger = get_logger('UpdateHelpChannel')

    def execute(self):
        # Pass the help channel id to the portal
        # Hit the response URL w/ an update (success or failure)

        self.logger.info(f'Executing UpdateHelpChannel for {self.team_id} with user {self.installer_id}')
        self.slack_client_wrapper.send_dm_to_user(slack_team_id=self.team_id, slack_user_id=self.installer_id,
                                                  text=ONBOARDING_DM.text, attachments=[ONBOARDING_DM.attachment])
