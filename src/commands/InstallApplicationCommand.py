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
        # TODO implement docstring
