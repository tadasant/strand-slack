from src.command.Command import Command
from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM


class CloseDiscussionOnPortalCommand(Command):
    def __init__(self, portal_client_wrapper, slack_channel_id, slack_team_id):
        super().__init__(portal_client_wrapper=portal_client_wrapper, slack_team_id=slack_team_id)
        self.slack_channel_id = slack_channel_id

    def execute(self):
        """
            Send a message to the installer user with options for what s/he needs
            to fill out prior to activating the agent
        """
        log_msg = f'Executing CloseDiscussionOnPortalCommand for {self.slack_team_id} for chan {self.slack_channel_id}'
        self.logger.info(log_msg)
        self.portal_client_wrapper.close_discussion(slack_channel_id=self.slack_channel_id)
