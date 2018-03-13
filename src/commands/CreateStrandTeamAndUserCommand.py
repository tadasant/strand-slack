from src.commands.Command import Command
from src.utilities.database import db_session


class CreateStrandTeamAndUserCommand(Command):
    """
        1) Delegate to wrapper to create team with `team_id` and `team_name`
        2) Update Agent.strand_team_id
        3) Delegate to wrapper to create user with the new `strand_team_id`
    """

    def __init__(self, slack_team_id, slack_team_name, slack_user_id, strand_api_client_wrapper, slack_client_wrapper):
        super().__init__(strand_api_client_wrapper=strand_api_client_wrapper, slack_client_wrapper=slack_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id
        self.slack_team_name = slack_team_name

    @db_session
    def execute(self, session):
        self.logger.debug(f'Creating strand team {self.slack_team_id} with name {self.slack_team_name}')
        # strand_team_id = self.strand_api_client_wrapper.create_team()
        # update db
        self.logger.debug(f'Creating strand user {self.slack_user_id} in strand team {strand_team_id}')
