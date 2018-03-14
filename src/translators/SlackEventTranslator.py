from src.translators.Translator import Translator


class SlackEventTranslator(Translator):
    def __init__(self, slack_event_request, slack_client_wrapper, strand_api_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper, strand_api_client_wrapper=strand_api_client_wrapper)
        self.slack_event_request = slack_event_request

    def translate(self):
        self.logger.debug(f'Translating slack_event_request {self.slack_event_request}')
        # Invoke service
        # slack_installation_service = SlackInstallationService(slack_event_request=self.slack_event_request,
        #                                                       slack_client_wrapper=self.slack_client_wrapper,
        #                                                       strand_api_client_wrapper=self.strand_api_client_wrapper)
        # Thread(target=slack_installation_service.execute, daemon=True).start()
