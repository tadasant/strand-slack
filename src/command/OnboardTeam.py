from src.command.messages.onboarding_dm import ONBOARDING_DM
from src.common.logging import get_logger


class OnboardTeam:
    def __init__(self, slack_client_wrapper, team_id, installer_id):
        self.slack_client_wrapper = slack_client_wrapper
        self.team_id = team_id
        self.installer_id = installer_id
        self.logger = get_logger('OnboardTeam')

    def execute(self):
        self.logger.info(f'Executing OnboardTeam for {self.team_id} with user {self.installer_id}')
        self.slack_client_wrapper.send_dm_to_user(slack_team_id=self.team_id, slack_user_id=self.installer_id,
                                                  text=ONBOARDING_DM['text'], attachments=[ONBOARDING_DM['attachment']])
        # send DM
        pass
