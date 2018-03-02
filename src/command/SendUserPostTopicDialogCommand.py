from src.command.Command import Command
from src.command.model.message.post_topic_dialog import POST_TOPIC_DIALOG, POST_TOPIC_DIALOG_WITH_CHANNEL_OPTION
from src.domain.repositories.SlackAgentRepository import slack_agent_repository


class SendUserPostTopicDialogCommand(Command):
    def __init__(self, slack_client_wrapper, trigger_id, slack_team_id, slack_user_id, slack_channel_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper, slack_team_id=slack_team_id)
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id
        self.trigger_id = trigger_id

    def execute(self):
        """Send user a dialog box to fill out for a new topic"""
        self.logger.info(f'Executing SendUserPostTopicDialog for {self.slack_team_id} with user {self.slack_user_id}')
        topic_channel_id = slack_agent_repository.get_topic_channel_id(self.slack_team_id)
        if self.slack_channel_id.startswith('C') and self.slack_channel_id != topic_channel_id:
            self.slack_client_wrapper.send_dialog(trigger_id=self.trigger_id, slack_team_id=self.slack_team_id,
                                                  dialog=POST_TOPIC_DIALOG_WITH_CHANNEL_OPTION.value)
        else:
            self.slack_client_wrapper.send_dialog(trigger_id=self.trigger_id, slack_team_id=self.slack_team_id,
                                                  dialog=POST_TOPIC_DIALOG.value)
