from src.command.Command import Command
from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM


class InitiateAgentOnboardingCommand(Command):
    def __init__(self, slack_client_wrapper, slack_team_id, installer_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper, slack_team_id=slack_team_id)
        self.installer_id = installer_id

    def execute(self):
        self.logger.info(f'Executing InitiateAgentOnboarding for {self.slack_team_id} with user {self.installer_id}')
        self.slack_client_wrapper.send_dm_to_user(slack_team_id=self.slack_team_id, slack_user_id=self.installer_id,
                                                  text=INITIAL_ONBOARDING_DM.text,
                                                  attachments=[INITIAL_ONBOARDING_DM.attachment])
