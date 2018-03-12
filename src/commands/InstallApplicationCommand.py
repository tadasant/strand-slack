from src import get_slack_client_wrapper
from src.commands.Command import Command


class InstallApplicationCommand(Command):
    """
        # Intentional: violating no-read-from-db rule to avoid excessive roundtrip

        1) Using `code`, calls Slack's oauth.access endpoint
        2) Slack response contains slack_team_id, which is checked against SLA DB's Agents
        3) If Agent exists and installer exists, we UPDATE User entry
        4) If Agent exists and installer does not exist, we INSERT User entry
        5) If team does not exist, we INSERT Agent and INSERT User
        6) Regardless of situation, User is sent a welcome message
    """

    def __init__(self, code):
        super().__init__()
        self.code = code

    def execute(self):
        self.logger.debug(f'Installing application with oauth code {self.code}')
        slack_oauth_access_response = get_slack_client_wrapper().submit_oauth_code(code=self.code)
        # TODO with db session
        if self._does_agent_exist(slack_team_id=slack_oauth_access_response.team_id):
            if self._does_installer_exist(slack_user_id=slack_oauth_access_response.user_id):
                self._update_installer(slack_oauth_access_response=slack_oauth_access_response)
            else:
                self._create_installer(slack_oauth_access_response=slack_oauth_access_response)
        else:
            self._create_agent(slack_oauth_access_response=slack_oauth_access_response)
            self._create_installer(slack_oauth_access_response=slack_oauth_access_response)
        self._send_installer_welcome_message(slack_team_id=slack_oauth_access_response.team_id,
                                             slack_user_id=slack_oauth_access_response.user_id)

    def _does_agent_exist(self, slack_team_id):
        # TODO
        pass

    def _does_installer_exist(self, slack_user_id):
        # TODO
        pass

    def _update_installer(self, slack_oauth_access_response):
        # TODO
        pass

    def _create_installer(self, slack_oauth_access_response):
        # TODO
        pass

    def _create_agent(self, slack_oauth_access_response):
        # TODO
        pass

    def _send_installer_welcome_message(self, slack_team_id, slack_user_id):
        get_slack_client_wrapper().send_dm_to_user(slack_team_id=slack_team_id, slack_user_id=slack_user_id,
                                                   text='Successfully installed Strand!')
