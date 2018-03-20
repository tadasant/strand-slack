from threading import Thread

from src.commands.Command import Command
from src.commands.CreateStrandTeamWithUserCommand import CreateStrandTeamWithUserCommand
from src.commands.AddStrandUserToTeamCommand import AddStrandUserToTeamCommand
from src.models.domain.Agent import Agent, AgentStatus
from src.models.domain.Bot import Bot
from src.models.domain.Installation import Installation
from src.models.domain.User import User
from src.models.slack.outgoing.messages import WelcomeSlackMessage
from src.utilities.database import db_session


class InstallApplicationCommand(Command):
    """
        # Intentional: violating no-read-from-db rule to avoid excessive roundtrip

        1) Using `code`, calls Slack's oauth.access endpoint
        2) Slack response contains slack_team_id, which is checked against SLA DB's Agents
        3) Agent, User (installer), Installation are created or updated
        4) If relevant, commands for forwarding Agent and User to Strand API are kicked off
        5) User is sent a welcome message
    """

    def __init__(self, code, slack_client_wrapper, strand_api_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper, strand_api_client_wrapper=strand_api_client_wrapper)
        self.code = code

    @db_session
    def execute(self, session):
        self.logger.debug(f'Installing application with oauth code {self.code}')
        slack_oauth_access_response = self.slack_client_wrapper.submit_oauth_code(code=self.code)
        does_agent_exist = self._does_agent_exist(slack_oauth_access_response=slack_oauth_access_response,
                                                  session=session)
        does_installer_exist = self._does_installer_exist(slack_oauth_access_response=slack_oauth_access_response,
                                                          session=session)
        does_installation_exist = self._does_installation_exist(slack_oauth_access_response=slack_oauth_access_response,
                                                                session=session)

        if not does_agent_exist:
            self._create_agent(slack_oauth_access_response=slack_oauth_access_response, session=session)
            self._create_installer(slack_oauth_access_response=slack_oauth_access_response, session=session)
            self._create_installation(slack_oauth_access_response=slack_oauth_access_response, session=session)
        elif not does_installer_exist:
            self._create_installer(slack_oauth_access_response=slack_oauth_access_response, session=session)
            self._create_installation(slack_oauth_access_response=slack_oauth_access_response, session=session)
        elif not does_installation_exist:
            self._create_installation(slack_oauth_access_response=slack_oauth_access_response, session=session)
        else:
            self._update_installation(slack_oauth_access_response=slack_oauth_access_response, session=session)

        # ensure DB commit before communicating with Strand API
        session.commit()

        if not does_agent_exist:
            command = CreateStrandTeamWithUserCommand(
                slack_team_id=slack_oauth_access_response.team_id,
                slack_team_name=slack_oauth_access_response.team_name,
                slack_user_id=slack_oauth_access_response.user_id,
                strand_api_client_wrapper=self.strand_api_client_wrapper,
                slack_client_wrapper=self.slack_client_wrapper
            )
            Thread(target=command.execute, daemon=True).start()
        elif not does_installer_exist:
            command = AddStrandUserToTeamCommand(
                slack_team_id=slack_oauth_access_response.team_id,
                slack_user_id=slack_oauth_access_response.user_id,
                strand_team_id=self._get_strand_team_id(slack_oauth_access_response=slack_oauth_access_response,
                                                        session=session),
                strand_api_client_wrapper=self.strand_api_client_wrapper,
                slack_client_wrapper=self.slack_client_wrapper
            )
            Thread(target=command.execute, daemon=True).start()

        self._send_installer_welcome_message(slack_oauth_access_response=slack_oauth_access_response)

    @staticmethod
    def _get_strand_team_id(slack_oauth_access_response, session):
        return session.query(Agent).filter(
            Agent.slack_team_id == slack_oauth_access_response.team_id).one().strand_team_id

    @staticmethod
    def _does_agent_exist(slack_oauth_access_response, session):
        slack_team_id = slack_oauth_access_response.team_id
        agent = session.query(Agent).filter(Agent.slack_team_id == slack_team_id).one_or_none()
        return agent is not None

    @staticmethod
    def _create_agent(slack_oauth_access_response, session):
        bot = Bot(access_token=slack_oauth_access_response.bot.bot_access_token,
                  user_id=slack_oauth_access_response.bot.bot_user_id,
                  agent_slack_team_id=slack_oauth_access_response.team_id)
        agent = Agent(slack_team_id=slack_oauth_access_response.team_id, status=AgentStatus.ACTIVE.name, bot=bot)
        session.add_all([bot, agent])

    @staticmethod
    def _does_installer_exist(slack_oauth_access_response, session):
        slack_team_id = slack_oauth_access_response.team_id
        slack_user_id = slack_oauth_access_response.user_id
        installer = session.query(User).filter(
            User.agent_slack_team_id == slack_team_id,
            User.slack_user_id == slack_user_id).one_or_none()
        return installer is not None

    @staticmethod
    def _create_installer(slack_oauth_access_response, session):
        installer = User(slack_user_id=slack_oauth_access_response.user_id,
                         agent_slack_team_id=slack_oauth_access_response.team_id)
        session.add(installer)

    @staticmethod
    def _does_installation_exist(slack_oauth_access_response, session):
        slack_team_id = slack_oauth_access_response.team_id
        slack_user_id = slack_oauth_access_response.user_id
        installation = session.query(Installation).filter(
            Installation.installer_slack_user_id == slack_user_id,
            Installation.installer_agent_slack_team_id == slack_team_id).one_or_none()
        return installation is not None

    @staticmethod
    def _create_installation(slack_oauth_access_response, session):
        installation = Installation(access_token=slack_oauth_access_response.access_token,
                                    scope=slack_oauth_access_response.scope,
                                    installer_slack_user_id=slack_oauth_access_response.user_id,
                                    installer_agent_slack_team_id=slack_oauth_access_response.team_id)
        session.add(installation)

    @staticmethod
    def _update_installation(slack_oauth_access_response, session):
        installation = session.query(Installation).filter(
            Installation.installer_slack_user_id == slack_oauth_access_response.user_id,
            Installation.installer_agent_slack_team_id == slack_oauth_access_response.team_id).one()
        installation.access_token = slack_oauth_access_response.access_token
        installation.scope = slack_oauth_access_response.scope

    def _send_installer_welcome_message(self, slack_oauth_access_response):
        slack_team_id = slack_oauth_access_response.team_id
        slack_user_id = slack_oauth_access_response.user_id
        self.slack_client_wrapper.send_dm_to_user(slack_team_id=slack_team_id, slack_user_id=slack_user_id,
                                                  text=WelcomeSlackMessage().text)
