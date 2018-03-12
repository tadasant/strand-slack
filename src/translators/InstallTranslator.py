from threading import Thread

from src.services.parent.SlackInstallationService import SlackInstallationService
from src.translators.Translator import Translator


class InstallTranslator(Translator):
    def __init__(self, code):
        super().__init__()
        self.code = code

    def translate(self):
        self.logger.debug(f'Translating code {self.code}')
        slack_installation_service = SlackInstallationService(code=self.code)
        Thread(target=slack_installation_service.execute, daemon=True).start()
