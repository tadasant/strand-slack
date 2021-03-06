import re
from threading import Thread

from src.translators.Translator import Translator
from src.services.parent.InitiateSaveStrandViaSlashCommandService import InitiateSaveStrandViaSlashCommandService
from src.services.parent.ProvideHelpService import ProvideHelpService


class SlackSlashCommandTranslator(Translator):
    def __init__(self, slack_slash_command_request, slack_client_wrapper, strand_api_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper, strand_api_client_wrapper=strand_api_client_wrapper)
        self.slack_slash_command_request = slack_slash_command_request

    def translate(self):
        self.logger.debug(f'Translating slack_slash_command_request: {self.slack_slash_command_request}')
        text = self.slack_slash_command_request.text
        slack_team_id = self.slack_slash_command_request.team_id
        slack_user_id = self.slack_slash_command_request.user_id
        slack_channel_id = self.slack_slash_command_request.channel_id

        if self.slack_slash_command_request.is_strand_command:
            if self.slack_slash_command_request.is_save_command:
                start_phrase = re.sub(r'(“|”|save)', '', text).strip()
                service = InitiateSaveStrandViaSlashCommandService(slack_team_id=slack_team_id,
                                                                   slack_user_id=slack_user_id,
                                                                   slack_channel_id=slack_channel_id,
                                                                   start_phrase=start_phrase,
                                                                   slack_client_wrapper=self.slack_client_wrapper,
                                                                   strand_api_client_wrapper=self.
                                                                   strand_api_client_wrapper)
                Thread(target=service.execute, daemon=True).start()
            else:
                service = ProvideHelpService(slack_client_wrapper=self.slack_client_wrapper,
                                             slack_team_id=slack_team_id,
                                             slack_user_id=slack_user_id,
                                             slack_channel_id=slack_channel_id)
                Thread(target=service.execute, daemon=True).start()
        else:
            self.logger.debug('Ignoring slash command request.')
