from threading import Thread

from src.commands.AddStrandUserToTeamCommand import AddStrandUserToTeamCommand
from src.commands.Command import Command
from src.commands.CreateStrandTeamWithUserCommand import CreateStrandTeamWithUserCommand
from src.models.domain.Agent import Agent, AgentStatus
from src.models.domain.Bot import Bot
from src.models.domain.Installation import Installation
from src.models.domain.User import User
from src.models.slack.outgoing.messages import WelcomeSlackMessage
from src.models.slack.responses.SlackOauthAccessResponse import SlackOauthAccessResponse
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
        response: SlackOauthAccessResponse = self.slack_client_wrapper.submit_oauth_code(code=self.code)
        existing_agent = self._get_agent(slack_oauth_access_response=response,
                                         session=session)
        existing_installer = self._get_installer(slack_oauth_access_response=response,
                                                 session=session)
        existing_installation = self._get_installation(slack_oauth_access_response=response,
                                                       session=session)
        existing_bot = self._get_bot(slack_oauth_access_response=response, session=session)

        if existing_bot and response.bot:
            # An updated bot has been sent
            self._update_bot(slack_oauth_access_response=response, session=session)

        if not existing_agent:
            self._create_agent_and_bot(slack_oauth_access_response=response, session=session)
            self._create_installer(slack_oauth_access_response=response, session=session)
            self._create_installation(slack_oauth_access_response=response, session=session)
        elif not existing_installer:
            self._create_installer(slack_oauth_access_response=response, session=session)
            self._create_installation(slack_oauth_access_response=response, session=session)
        elif not existing_installation:
            self._create_installation(slack_oauth_access_response=response, session=session)
        else:
            self._update_installation(slack_oauth_access_response=response, session=session)

        # ensure DB commit before communicating with Strand API
        session.commit()

        if not existing_agent or not existing_agent.strand_team_id:
            command = CreateStrandTeamWithUserCommand(
                slack_team_id=response.team_id,
                slack_team_name=response.team_name,
                slack_user_id=response.user_id,
                strand_api_client_wrapper=self.strand_api_client_wrapper,
                slack_client_wrapper=self.slack_client_wrapper
            )
            Thread(target=command.execute, daemon=True).start()
        elif not existing_installer or not existing_installer.strand_user_id:
            command = AddStrandUserToTeamCommand(
                slack_team_id=response.team_id,
                slack_user_id=response.user_id,
                strand_team_id=self._get_strand_team_id(slack_oauth_access_response=response,
                                                        session=session),
                strand_api_client_wrapper=self.strand_api_client_wrapper,
                slack_client_wrapper=self.slack_client_wrapper
            )
            Thread(target=command.execute, daemon=True).start()

        self._send_installer_welcome_message(slack_oauth_access_response=response)

    @staticmethod
    def _get_strand_team_id(slack_oauth_access_response, session):
        return session.query(Agent).filter(
            Agent.slack_team_id == slack_oauth_access_response.team_id).one().strand_team_id

    @staticmethod
    def _get_agent(slack_oauth_access_response, session) -> Agent:
        slack_team_id = slack_oauth_access_response.team_id
        agent = session.query(Agent).filter(Agent.slack_team_id == slack_team_id).one_or_none()
        return agent

    @staticmethod
    def _create_agent_and_bot(slack_oauth_access_response, session):
        bot = Bot(access_token=slack_oauth_access_response.bot.bot_access_token,
                  user_id=slack_oauth_access_response.bot.bot_user_id,
                  agent_slack_team_id=slack_oauth_access_response.team_id)
        agent = Agent(slack_team_id=slack_oauth_access_response.team_id, status=AgentStatus.ACTIVE.name, bot=bot)
        session.add_all([bot, agent])

    @staticmethod
    def _get_installer(slack_oauth_access_response, session) -> User:
        slack_team_id = slack_oauth_access_response.team_id
        slack_user_id = slack_oauth_access_response.user_id
        installer = session.query(User).filter(
            User.agent_slack_team_id == slack_team_id,
            User.slack_user_id == slack_user_id).one_or_none()
        return installer

    @staticmethod
    def _create_installer(slack_oauth_access_response, session):
        installer = User(slack_user_id=slack_oauth_access_response.user_id,
                         agent_slack_team_id=slack_oauth_access_response.team_id)
        session.add(installer)

    @staticmethod
    def _get_installation(slack_oauth_access_response, session) -> Installation:
        slack_team_id = slack_oauth_access_response.team_id
        slack_user_id = slack_oauth_access_response.user_id
        installation = session.query(Installation).filter(
            Installation.installer_slack_user_id == slack_user_id,
            Installation.installer_agent_slack_team_id == slack_team_id).one_or_none()
        return installation

    @staticmethod
    def _create_installation(slack_oauth_access_response, session):
        installation = Installation(access_token=slack_oauth_access_response.access_token,
                                    scope=slack_oauth_access_response.scope,
                                    installer_slack_user_id=slack_oauth_access_response.user_id,
                                    installer_agent_slack_team_id=slack_oauth_access_response.team_id)
        session.add(installation)

    def _update_installation(self, slack_oauth_access_response, session):
        installation = self._get_installation(slack_oauth_access_response=slack_oauth_access_response, session=session)
        installation.access_token = slack_oauth_access_response.access_token
        installation.scope = slack_oauth_access_response.scope

    @staticmethod
    def _get_bot(slack_oauth_access_response, session) -> Bot:
        slack_team_id = slack_oauth_access_response.team_id
        bot = session.query(Bot).filter(Bot.agent_slack_team_id == slack_team_id).one_or_none()
        return bot

    def _update_bot(self, slack_oauth_access_response, session):
        bot = self._get_bot(slack_oauth_access_response=slack_oauth_access_response, session=session)
        bot.access_token = slack_oauth_access_response.bot.bot_access_token
        bot.user_id = slack_oauth_access_response.bot.bot_user_id

    def _send_installer_welcome_message(self, slack_oauth_access_response):
        slack_team_id = slack_oauth_access_response.team_id
        slack_user_id = slack_oauth_access_response.user_id
        self.slack_client_wrapper.send_dm_to_user(slack_team_id=slack_team_id, slack_user_id=slack_user_id,
                                                  text=WelcomeSlackMessage().text)
