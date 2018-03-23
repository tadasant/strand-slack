from threading import Thread

from src.models.slack.requests.SlackEventRequest import SlackEventRequest
from src.services.parent.InitiateSaveStrandService import InitiateSaveStrandService
from src.services.parent.ProvideHelpService import ProvideHelpService
from src.services.parent.RevokeTokensService import RevokeTokensService
from src.services.parent.UninstallAppService import UninstallAppService
from src.translators.Translator import Translator


class SlackEventTranslator(Translator):
    def __init__(self, slack_event_request, slack_client_wrapper, strand_api_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper, strand_api_client_wrapper=strand_api_client_wrapper)
        self.slack_event_request: SlackEventRequest = slack_event_request

    def translate(self):
        self.logger.debug(f'Translating slack_event_request {self.slack_event_request}')
        if self.slack_event_request.event and self.slack_event_request.event.is_message_dm_event:
            self.logger.info('Processing DM')
            slack_user_id = self.slack_event_request.event.user
            slack_channel_id = self.slack_event_request.event.channel
            slack_team_id = self.slack_event_request.team_id
            if self.slack_event_request.event.is_help_dm_event:
                service = ProvideHelpService(slack_client_wrapper=self.slack_client_wrapper,
                                             slack_team_id=slack_team_id,
                                             slack_user_id=slack_user_id,
                                             slack_channel_id=slack_channel_id)
                Thread(target=service.execute, daemon=True).start()
            else:
                text = self.slack_event_request.event.text
                service = InitiateSaveStrandService(slack_client_wrapper=self.slack_client_wrapper,
                                                    strand_api_client_wrapper=self.strand_api_client_wrapper,
                                                    text=text,
                                                    slack_team_id=slack_team_id,
                                                    slack_user_id=slack_user_id,
                                                    slack_channel_id=slack_channel_id)
                Thread(target=service.execute, daemon=True).start()
        elif self.slack_event_request.event and self.slack_event_request.event.is_tokens_revoked_event:
            service = RevokeTokensService(slack_team_id=self.slack_event_request.team_id,
                                          oauth_tokens=self.slack_event_request.event.tokens.oauth,
                                          bot_tokens=self.slack_event_request.event.tokens.bot)
            Thread(target=service.execute, daemon=True).start()
        elif self.slack_event_request.event and self.slack_event_request.event.is_app_uninstalled_event:
            service = UninstallAppService(slack_team_id=self.slack_event_request.team_id)
            Thread(target=service.execute, daemon=True).start()
        else:
            self.logger.debug('Ignoring event.')
