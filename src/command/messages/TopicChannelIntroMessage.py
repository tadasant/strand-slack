from textwrap import dedent


class TopicChannelIntroMessage:
    """Message that sits at the bottom of the topic channel"""

    def __init__(self, is_update=True):
        """is_update should be False only on the first-ever topic channel post"""
        self._is_update = is_update

        self.text = self._format_text()
        self.attachments = self._format_attachments()

    @property
    def post_new_topic_button(self):
        return {
            'fallback': f'Can\'t display the button, please use `/codeclippy post`',
            "callback_id": "post_new_topic",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "post",
                    "text": "Post new topic",
                    "style": "primary",
                    "type": "button",
                    "value": "post"
                }
            ]
        }

    def _format_text(self):
        new_topic_text = '_I updated my last message with a new topic for discussion, check it out!_ :fire:\n'
        new_topic_prepended = new_topic_text if self._is_update else ''
        return dedent(f'''
            {new_topic_prepended}
            _This channel is a live view of the topics of all discussions going on right now._

             Type `/codeclippy post`, or click below to start another one!
        ''')

    def _format_attachments(self):
        return [self.post_new_topic_button]
