from threading import Thread

from src.commands.ForwardSavedStrandAndInformUserCommand import ForwardSavedStrandAndInformUserCommand
from src.commands.SendPleaseInstallMessageCommand import SendPleaseInstallMessageCommand
from src.models.exceptions.exceptions import InvalidSlashCommandException
from src.models.domain.Agent import Agent
from src.models.domain.User import User
from src.services.Service import Service
from src.services.helper.BuildTextFromChannelHistoryService import BuildTextFromChannelHistoryService
from src.services.helper.ConvertTextToGFMService import ConvertTextToGFMService
from src.utilities.database import db_session


class InitiateSaveStrandViaSlashCommandService(Service):
    def __init__(self, slack_team_id, slack_user_id, slack_channel_id, start_phrase,
                 slack_client_wrapper, strand_api_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper, strand_api_client_wrapper=strand_api_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id
        self.start_phrase = start_phrase

    @db_session
    def execute(self, session):
        if User.is_installer(session, self.slack_user_id, self.slack_team_id):
            try:
                text = BuildTextFromChannelHistoryService(start_phrase=self.start_phrase,
                                                          slack_channel_id=self.slack_channel_id,
                                                          slack_team_id=self.slack_team_id,
                                                          slack_user_id=self.slack_user_id,
                                                          slack_client_wrapper=self.slack_client_wrapper).execute()
                markdown_body = ConvertTextToGFMService(text=text,
                                                        slack_client_wrapper=self.slack_client_wrapper).execute()
                strand_team_id = Agent.get_strand_team_id(session, self.slack_team_id)
                saver_strand_user_id = self._get_saver_strand_user_id(session)
                command = ForwardSavedStrandAndInformUserCommand(
                    slack_client_wrapper=self.slack_client_wrapper,
                    strand_api_client_wrapper=self.strand_api_client_wrapper,
                    strand_team_id=strand_team_id,
                    slack_team_id=self.slack_team_id,
                    saver_strand_user_id=saver_strand_user_id,
                    body=markdown_body,
                    slack_channel_id=self.slack_channel_id,
                    slack_user_id=self.slack_user_id,
                    use_ephemeral=True
                )
                Thread(target=command.execute, daemon=True).start()
            except InvalidSlashCommandException as e:
                # TODO: [SLA-185] Send error message that messages could not be pulled for whatever reason
                self.logger.error(e)
        else:
            command = SendPleaseInstallMessageCommand(slack_client_wrapper=self.slack_client_wrapper,
                                                      slack_team_id=self.slack_team_id,
                                                      slack_user_id=self.slack_user_id,
                                                      slack_channel_id=self.slack_channel_id)
            Thread(target=command.execute, daemon=True).start()

    def _get_saver_strand_user_id(self, session):
        return session.query(User).filter(User.agent_slack_team_id == self.slack_team_id,
                                          User.slack_user_id == self.slack_user_id).one().strand_user_id
