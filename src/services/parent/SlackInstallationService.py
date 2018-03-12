from threading import Thread

from src.commands.InstallApplicationCommand import InstallApplicationCommand
from src.services.Service import Service


class SlackInstallationService(Service):
    def __init__(self, code):
        super().__init__()
        self.code = code

    def execute(self):
        self.logger.debug(f'Installing Slack app with oauth code {self.code}')
        install_application_command = InstallApplicationCommand(code=self.code)
        Thread(target=install_application_command.execute, daemon=True).start()
