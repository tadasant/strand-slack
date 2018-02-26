from src.domain.repositories.SlackAgentRepository import slack_agent_repository
from src.command.Command import Command
from src.command.model.message.message_models import HelpMessage


class SendHelpMessageCommand(Command):
    def __init__(self, slack_client_wrapper, slack_team_id, slack_user_id, slack_channel_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper, slack_team_id=slack_team_id)
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id

    def execute(self):
        self.logger.info(f'Executing SendHelpMessageCommand for {self.slack_team_id} with user {self.slack_user_id}')
        topic_channel_id = slack_agent_repository.get_topic_channel_id(slack_team_id=self.slack_team_id)
        self.slack_client_wrapper.send_ephemeral_message(slack_team_id=self.slack_team_id,
                                                         slack_channel_id=self.slack_channel_id,
                                                         slack_user_id=self.slack_user_id,
                                                         text=HelpMessage(topic_channel_id=topic_channel_id).text)
