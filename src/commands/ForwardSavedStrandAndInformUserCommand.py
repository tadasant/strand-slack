from src.commands.Command import Command
from src.models.slack.outgoing.messages import SavedStrandSlackMessage


class ForwardSavedStrandAndInformUserCommand(Command):
    """
        1) Send strand to Strand API
        2) Send metadata message prompt to user in Slack
    """

    def __init__(self, slack_client_wrapper, strand_api_client_wrapper, slack_team_id, strand_team_id,
                 saver_strand_user_id, body, slack_channel_id, slack_user_id, use_ephemeral=False, use_bot_token=True):
        super().__init__(slack_client_wrapper=slack_client_wrapper, strand_api_client_wrapper=strand_api_client_wrapper)
        self.strand_team_id = strand_team_id
        self.slack_team_id = slack_team_id
        self.saver_strand_user_id = saver_strand_user_id
        self.body = body
        self.slack_channel_id = slack_channel_id
        self.slack_user_id = slack_user_id
        self.use_ephemeral = use_ephemeral  # Should be True if via Slash command
        self.use_bot_token = use_bot_token  # Must be False if in a group, IM, or MPIM

    def execute(self):
        self.logger.info(f'Executing Forwa...Command for {self.strand_team_id} with user {self.saver_strand_user_id}')
        strand = self.strand_api_client_wrapper.create_strand(team_id=self.strand_team_id,
                                                              saver_user_id=self.saver_strand_user_id,
                                                              body=self.body)
        saved_strand_slack_message = SavedStrandSlackMessage(strand_id=strand.id)
        if self.use_ephemeral:
            self.slack_client_wrapper.send_ephemeral_message(slack_team_id=self.slack_team_id,
                                                             slack_channel_id=self.slack_channel_id,
                                                             slack_user_id=self.slack_user_id,
                                                             text=saved_strand_slack_message.text,
                                                             attachments=saved_strand_slack_message.attachments,
                                                             use_bot_token=self.use_bot_token)
        else:
            self.slack_client_wrapper.send_message(slack_team_id=self.slack_team_id,
                                                   slack_channel_id=self.slack_channel_id,
                                                   text=saved_strand_slack_message.text,
                                                   attachments=saved_strand_slack_message.attachments)
