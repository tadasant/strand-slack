from threading import Thread

from src.commands.InstallApplicationCommand import InstallApplicationCommand
from src.services.Service import Service


class SlackInstallationService(Service):
    def __init__(self, code, slack_client_wrapper, strand_api_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper, strand_api_client_wrapper=strand_api_client_wrapper)
        self.code = code

    def execute(self):
        self.logger.debug(f'Installing Slack app with oauth code {self.code}')
        install_application_command = InstallApplicationCommand(code=self.code,
                                                                slack_client_wrapper=self.slack_client_wrapper,
                                                                strand_api_client_wrapper=self.strand_api_client_wrapper)
        Thread(target=install_application_command.execute, daemon=True).start()
