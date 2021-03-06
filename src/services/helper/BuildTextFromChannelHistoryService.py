from datetime import datetime

from fuzzywuzzy import fuzz

from src.models.exceptions.exceptions import InvalidSlashCommandException
from src.services.Service import Service


class BuildTextFromChannelHistoryService(Service):
    """Given text with a time-range of messages in a channel, build text"""

    def __init__(self, start_phrase, slack_channel_id, slack_team_id, slack_user_id, slack_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper)
        self.start_phrase = start_phrase
        self.slack_channel_id = slack_channel_id
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id

    def execute(self):
        """Parse command text, pull messages in range, return as body of text"""
        messages = self.slack_client_wrapper.get_channel_history(slack_channel_id=self.slack_channel_id,
                                                                 slack_team_id=self.slack_team_id,
                                                                 slack_user_id=self.slack_user_id)
        messages = self._splice_messages(messages, start_phrase=self.start_phrase, default=10)
        text = '\n\n'.join([self._format_message(message) for message in messages])
        return text

    def _splice_messages(self, messages, start_phrase=None, default=10):
        """Take full channel history and splice into the intended subset.

        If no start phrase is provided, the default number of latest messages are returned.

        If a start phrase is provided and a message matches with > 85% accuracy, we return
        all messages corresponding messages including the matching message.

        If a start phrase is provided and no messages matches with a > 85% accuracy, we raise
        an InvalidSlashCommandException that explains that the start phrase given does not
        match any available messages in the current channel.
        """
        if not start_phrase:
            return reversed(messages[:default])

        for idx, message in enumerate(messages):
            if fuzz.ratio(message.text[:len(start_phrase)].lower(), start_phrase.lower()) > 85:
                return reversed(messages[:idx + 1])

        raise InvalidSlashCommandException(message=f'Cannot find message matching start phrase: {start_phrase}')

    def _format_message(self, message):
        """Takes a message object and returns a formatted body resembling copy-and-pasting."""
        time = datetime.fromtimestamp(int(message.ts.split('.')[0])).strftime('%l:%M %p').strip()  # (e.g. "2:47 PM")
        header = f'USERNAME [{time}]'
        body = message.text
        return f'{header}\n{body}'
