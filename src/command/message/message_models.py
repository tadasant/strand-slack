from textwrap import dedent

from src.command.attachment.attachments import TOPIC_CHANNEL_ACTIONS_ATTACHMENT
from src.command.message.Message import Message


class TopicChannelIntroMessage(Message):
    """Message that sits at the bottom of the topic channel"""

    def __init__(self, is_update=True):
        """is_update should be False only on the first-ever topic channel post"""
        self._is_update = is_update

        super().__init__(
            text=self._format_text(),
            attachments=self._format_attachments()
        )

    def _format_text(self):
        new_topic_text = '_I updated my last message with a new topic for discussion, check it out!_ :fire:\n'
        new_topic_prepended = new_topic_text if self._is_update else ''
        return dedent(f'''
            {new_topic_prepended}
            _This channel is a live view of the topics of all discussions going on right now._

             Type `/codeclippy post`, or click below to start another one!
        ''')

    def _format_attachments(self):
        return [TOPIC_CHANNEL_ACTIONS_ATTACHMENT.as_dict()]
