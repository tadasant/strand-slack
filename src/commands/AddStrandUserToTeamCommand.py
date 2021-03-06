from src.commands.Command import Command
from src.models.domain.User import User
from src.utilities.database import db_session


class AddStrandUserToTeamCommand(Command):
    """
        1) Grab additional user info from Slack
        2) Either create user with the team, or just attach existing user to the team
        3) Update User.strand_user_id
    """

    def __init__(self, slack_team_id, slack_user_id, strand_team_id, strand_api_client_wrapper, slack_client_wrapper):
        super().__init__(strand_api_client_wrapper=strand_api_client_wrapper, slack_client_wrapper=slack_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id
        self.strand_team_id = strand_team_id

    @db_session
    def execute(self, session):
        log_msg = f'Creating user {self.slack_user_id} on strand team {self.strand_team_id}'
        self.logger.debug(log_msg)
        slack_user = self.slack_client_wrapper.get_user_info(slack_team_id=self.slack_team_id,
                                                             slack_user_id=self.slack_user_id)
        real_name_tokens = slack_user.profile.real_name.split(' ')
        first_name = real_name_tokens[0]
        last_name = real_name_tokens[-1] if len(real_name_tokens) > 1 else ''
        strand_user = self.strand_api_client_wrapper.get_user_by_email(email=slack_user.profile.email)
        if strand_user:
            # Strand API has seen this user email before
            self.strand_api_client_wrapper.add_user_to_team(user_id=strand_user.id,
                                                                          team_id=self.strand_team_id)
        else:
            strand_user = self.strand_api_client_wrapper.create_user_with_team(email=slack_user.profile.email,
                                                                               first_name=first_name,
                                                                               last_name=last_name,
                                                                               team_id=self.strand_team_id)
        self._update_user(slack_user_id=self.slack_user_id, strand_user_id=strand_user.id, session=session)

    @staticmethod
    def _update_user(slack_user_id, strand_user_id, session):
        user = session.query(User).filter(User.slack_user_id == slack_user_id).one()
        user.strand_user_id = strand_user_id
