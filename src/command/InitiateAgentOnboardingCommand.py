from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM
from src.common.logging import get_logger


class InitiateAgentOnboardingCommand:
    def __init__(self, slack_client_wrapper, team_id, installer_id):
        self.slack_client_wrapper = slack_client_wrapper
        self.team_id = team_id
        self.installer_id = installer_id
        self.logger = get_logger('InitiateAgentOnboarding')

    def execute(self):
        self.logger.info(f'Executing InitiateAgentOnboarding for {self.team_id} with user {self.installer_id}')
        self.slack_client_wrapper.send_dm_to_user(slack_team_id=self.team_id, slack_user_id=self.installer_id,
                                                  text=INITIAL_ONBOARDING_DM.text, attachments=[INITIAL_ONBOARDING_DM.attachment])
