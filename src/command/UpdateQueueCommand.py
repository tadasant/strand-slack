from src.command.Command import Command


class UpdateQueueCommand(Command):
    def __init__(self, slack_client_wrapper, topic_slack_channel_id, discussion_slack_channel_id, slack_team_id,
                 slack_user_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper, slack_team_id=slack_team_id)
        self.topic_slack_channel_id = topic_slack_channel_id
        self.discussion_slack_channel_id = discussion_slack_channel_id
        self.slack_user_id = slack_user_id

    def execute(self):
        log_msg = f'Executing UpdateQueueCommand for {self.slack_team_id} for chan {self.discussion_slack_channel_id}'
        self.logger.info(log_msg)
        # TODO eventually remove this in favor of a modeled queue
        messages_info = self.slack_client_wrapper.get_channel_messages(slack_team_id=self.slack_team_id,
                                                                       slack_channel_id=self.topic_slack_channel_id)
        potential_entry_matches = [x for x in messages_info if self.discussion_slack_channel_id in x['text']]
        assert 1 == len(potential_entry_matches), 'Should have one entry per discussion channel in the queue'

        entry_ts = potential_entry_matches[0]['ts']
        entry_original_text = potential_entry_matches[0]['text']
        new_text = f'~{entry_original_text}~'  # strikeout

        self.slack_client_wrapper.update_message(slack_team_id=self.slack_team_id,
                                                 slack_channel_id=self.topic_slack_channel_id, new_text=new_text,
                                                 message_ts=entry_ts)
