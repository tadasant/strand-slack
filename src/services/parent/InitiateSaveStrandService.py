from src.services.Service import Service


class InitiateSaveStrandService(Service):
    def __init__(self, slack_team_id, slack_user_id, slack_channel_id, text, slack_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id
        self.text = text

    def execute(self):
        log_msg = f'Saving Strand with body {self.text} for user {self.slack_user_id} on team {self.slack_team_id}'
        self.logger.debug(log_msg)

        # install_application_command = InstallApplicationCommand(
        #     code=self.code,
        #     slack_client_wrapper=self.slack_client_wrapper,
        #     strand_api_client_wrapper=self.strand_api_client_wrapper
        # )
        # Thread(target=install_application_command.execute, daemon=True).start()
