from src.common.logging import get_logger


class OnboardTeam:
    def __init__(self, slack_client_wrapper, team_id, installer_id):
        self.slack_client_wrapper = slack_client_wrapper
        self.team_id = team_id
        self.installer_id = installer_id
        self.logger = get_logger('OnboardTeam')

    def execute(self):
        self.logger.info(f'Executing OnboardTeam for {self.team_id} with user {self.installer_id}')
        # send DM
        pass