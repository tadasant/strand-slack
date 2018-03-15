from threading import Thread

from src.services.parent.EditStrandMetadataService import EditStrandMetadataService
from src.translators.Translator import Translator


class SlackInteractiveComponentTranslator(Translator):
    def __init__(self, slack_interactive_component_request, slack_client_wrapper, strand_api_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper, strand_api_client_wrapper=strand_api_client_wrapper)
        self.slack_interactive_component_request = slack_interactive_component_request

    def translate(self):
        self.logger.debug(f'Translating slack_interactive_component_request {self.slack_interactive_component_request}')
        if self.slack_interactive_component_request.is_edit_metadata_button:
            trigger_id = self.slack_interactive_component_request.trigger_id
            slack_team_id = self.slack_interactive_component_request.team.id
            strand_id = self.slack_interactive_component_request.actions[0].value
            service = EditStrandMetadataService(slack_client_wrapper=self.slack_client_wrapper, trigger_id=trigger_id,
                                                slack_team_id=slack_team_id, strand_id=strand_id)
            Thread(target=service.execute, daemon=True).start()
        else:
            self.logger.debug('Ignoring interactive component request.')
