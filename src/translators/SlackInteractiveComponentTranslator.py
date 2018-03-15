from threading import Thread

from src.models.strand.StrandStrand import StrandStrand
from src.models.strand.StrandTag import StrandTag
from src.services.parent.EditStrandMetadataService import EditStrandMetadataService
from src.services.parent.SubmitStrandMetadataService import SubmitStrandMetadataService
from src.translators.Translator import Translator


class SlackInteractiveComponentTranslator(Translator):
    def __init__(self, slack_interactive_component_request, slack_client_wrapper, strand_api_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper, strand_api_client_wrapper=strand_api_client_wrapper)
        self.slack_interactive_component_request = slack_interactive_component_request

    def translate(self):
        self.logger.debug(f'Translating slack_interactive_component_request {self.slack_interactive_component_request}')
        slack_team_id = self.slack_interactive_component_request.team.id
        if self.slack_interactive_component_request.is_edit_metadata_button:
            strand_id = self.slack_interactive_component_request.actions[0].value
            trigger_id = self.slack_interactive_component_request.trigger_id
            service = EditStrandMetadataService(slack_client_wrapper=self.slack_client_wrapper, trigger_id=trigger_id,
                                                slack_team_id=slack_team_id, strand_id=strand_id)
            Thread(target=service.execute, daemon=True).start()
        elif self.slack_interactive_component_request.is_edit_metadata_dialog_submission:
            # submission to strand
            tag_names = [x.lower().strip() for x in self.slack_interactive_component_request.submission.tags.split(',')]
            tags = [StrandTag(name=name) for name in tag_names]
            strand_id = self.slack_interactive_component_request.get_strand_id()
            strand = StrandStrand(id=strand_id, title=self.slack_interactive_component_request.submission.title,
                                  tags=tags)
            service = SubmitStrandMetadataService(slack_client_wrapper=self.slack_client_wrapper,
                                                  strand_api_client_wrapper=self.strand_api_client_wrapper,
                                                  slack_team_id=slack_team_id,
                                                  strand=strand,
                                                  slack_user_id=self.slack_interactive_component_request.user.id,
                                                  slack_channel_id=self.slack_interactive_component_request.channel.id)
            Thread(target=service.execute, daemon=True).start()
        else:
            self.logger.debug('Ignoring interactive component request.')
