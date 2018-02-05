from src.command.Command import Command
from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM


class CloseDiscussionOnPortalCommand(Command):
    def __init__(self, portal_client_wrapper, topic_id, slack_team_id):
        super().__init__(portal_client_wrapper=portal_client_wrapper, slack_team_id=slack_team_id)
        self.topic_id = topic_id

    def execute(self):
        """
            Send a message to the installer user with options for what s/he needs
            to fill out prior to activating the agent
        """
        self.logger.info(f'Executing CloseDiscussionOnPortalCommand for {self.slack_team_id} for topic {self.topic_id}')
        self.portal_client_wrapper.
        # tODO
