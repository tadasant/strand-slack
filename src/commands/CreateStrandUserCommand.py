from src.commands.Command import Command
from src.utilities.database import db_session


class CreateStrandUserCommand(Command):
    """
        1) Grab additional user info from Slack
        2) Delegate to wrapper to create user with retrieved info
        3) Update User.strand_user_id
    """

    def __init__(self, slack_team_id, slack_user_id, strand_team_id, strand_api_client_wrapper):
        super().__init__(strand_api_client_wrapper=strand_api_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id
        self.strand_team_id = strand_team_id

    @db_session
    def execute(self, session):
        log_msg = f'Creating user {self.slack_user_id} on strand team {self.strand_team_id}'
        self.logger.debug(log_msg)
        # strand_team_id = self.strand_api_client_wrapper.create_team()
        # update db
