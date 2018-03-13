from threading import Thread

from src.commands.Command import Command
from src.commands.AddStrandUserToTeamCommand import AddStrandUserToTeamCommand
from src.models.domain.Agent import Agent
from src.utilities.database import db_session


class CreateStrandTeamWithUserCommand(Command):
    """
        1) Delegate to wrapper to create team with `team_id` and `team_name`
        2) Update Agent.strand_team_id
        3) Delegate to command for adding user to the new team
    """

    def __init__(self, slack_team_id, slack_team_name, slack_user_id, strand_api_client_wrapper, slack_client_wrapper):
        super().__init__(strand_api_client_wrapper=strand_api_client_wrapper, slack_client_wrapper=slack_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id
        self.slack_team_name = slack_team_name

    @db_session
    def execute(self, session):
        self.logger.debug(f'Creating strand team {self.slack_team_id} with name {self.slack_team_name}')
        strand_team = self.strand_api_client_wrapper.create_team(name=self.slack_team_name)
        self._update_agent(slack_team_id=self.slack_team_id, strand_team_id=strand_team.id, session=session)
        command = AddStrandUserToTeamCommand(slack_team_id=self.slack_team_id, slack_user_id=self.slack_user_id,
                                             strand_team_id=strand_team.id,
                                             strand_api_client_wrapper=self.strand_api_client_wrapper,
                                             slack_client_wrapper=self.slack_client_wrapper)
        Thread(target=command.execute, daemon=True).start()

    @staticmethod
    def _update_agent(slack_team_id, strand_team_id, session):
        agent = session.query(Agent).filter(Agent.slack_team_id == slack_team_id).one()
        agent.strand_team_id = strand_team_id
