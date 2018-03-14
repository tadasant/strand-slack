from threading import Thread

from src.commands.ForwardSavedStrandAndPromptUserForMetadataCommand import \
    ForwardSavedStrandAndPromptUserForMetadataCommand
from src.commands.SendPleaseInstallMessageCommand import SendPleaseInstallMessageCommand
from src.models.domain.Agent import Agent
from src.models.domain.User import User
from src.services.Service import Service
from src.services.helper.ConvertTextToGFMService import ConvertTextToGFMService
from src.utilities.database import db_session


class InitiateSaveStrandService(Service):
    def __init__(self, slack_team_id, slack_user_id, slack_channel_id, text, slack_client_wrapper,
                 strand_api_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper, strand_api_client_wrapper=strand_api_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id
        self.text = text

    @db_session
    def execute(self, session):
        log_msg = f'Saving Strand with body {self.text} for user {self.slack_user_id} on team {self.slack_team_id}'
        self.logger.debug(log_msg)
        if User.is_installer(session, self.slack_user_id, self.slack_team_id):
            markdown_body = ConvertTextToGFMService(text=self.text,
                                                    slack_client_wrapper=self.slack_client_wrapper).execute()
            strand_team_id = self._get_strand_team_id(session)
            saver_strand_user_id = self._get_saver_strand_user_id(session)
            command = ForwardSavedStrandAndPromptUserForMetadataCommand(
                slack_client_wrapper=self.slack_client_wrapper,
                strand_api_client_wrapper=self.strand_api_client_wrapper,
                strand_team_id=strand_team_id,
                saver_strand_user_id=saver_strand_user_id,
                body=markdown_body
            )
            Thread(target=command.execute, daemon=True).start()
            pass
        else:
            command = SendPleaseInstallMessageCommand(slack_client_wrapper=self.slack_client_wrapper,
                                                      slack_team_id=self.slack_team_id,
                                                      slack_user_id=self.slack_user_id,
                                                      slack_channel_id=self.slack_channel_id)
            Thread(target=command.execute, daemon=True).start()

    def _get_strand_team_id(self, session):
        return session.query(Agent).filter(Agent.slack_team_id == self.slack_team_id).one().strand_team_id

    def _get_saver_strand_user_id(self, session):
        return session.query(User).filter(User.agent_slack_team_id == self.slack_team_id,
                                          User.slack_user_id == self.slack_user_id).one().strand_user_id
