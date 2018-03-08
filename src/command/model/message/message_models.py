import time
from textwrap import dedent

from src.command.model.attachment.attachments import TOPIC_CHANNEL_ACTIONS_ATTACHMENT, \
    DISCUSSION_INTRO_ACTIONS_ATTACHMENT
from src.command.model.message.Message import Message


class TopicShareMessage(Message):
    def __init__(self, original_poster_user_id, discussion_channel_id, title, tag_names):
        self._original_poster_user_id = original_poster_user_id
        self._discussion_channel_id = discussion_channel_id
        self._title = title
        self._tag_names = [x.lower() for x in tag_names]
        self._ts = time.time()

        self.text = self._format_text()
        self.attachments = self._format_attachments()
        super().__init__(text=self.text, attachments=self.attachments)

    def _format_text(self):
        return f'New topic posted. Join the discussion :arrow_right: <#{self._discussion_channel_id}>'

    def _format_attachments(self):
        return [self._format_title_attachment()]

    def _format_title_attachment(self):
        return {
            'fallback': f'*Title*: {self._title}',
            'color': '#32424a',
            'author_name': f'Posted by <@{self._original_poster_user_id}>',
            'title': self._title,
            'text': ", ".join(self._tag_names),
            'footer': 'Strand',
            'footer_icon': 'https://s3.amazonaws.com/strand-public-assets/strand-logo.png',
            'ts': self._ts
        }

    def as_dict(self):
        result = super().as_dict()
        result['attachments'] = self.attachments
        return result


class ChannelTopicShareMessage(TopicShareMessage):
    def __init__(self, original_poster_user_id, discussion_channel_id, title, tag_names):
        super().__init__(original_poster_user_id=original_poster_user_id, discussion_channel_id=discussion_channel_id,
                         title=title, tag_names=tag_names)

    def _format_text(self):
        return f'<@{self._original_poster_user_id}> just shared a topic with this channel. ' \
               f'Join the discussion :arrow_right: <#{self._discussion_channel_id}>'


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

             Type `/strand post`, or click below to start another one!
        ''')

    def _format_attachments(self):
        return [TOPIC_CHANNEL_ACTIONS_ATTACHMENT]


class DiscussionInitiationMessage(Message):
    def __init__(self, original_poster_slack_user_id, title, description, tags):
        super().__init__(
            text=self._format_text(original_poster_slack_user_id, title, description, tags),
            attachments=self._format_attachments()
        )

    def _format_text(self, original_poster_slack_user_id, title, description, tags):
        return dedent(f'''
            *OP*: <@{original_poster_slack_user_id}>
            *Title*: {title}
            *Description*: {description}
            *Tags*: {tags}

            <@{original_poster_slack_user_id}>: please `/strand close` this discussion when you are done

            Do not post sensitive information! Transcripts of these discussions are stored.
        ''')

    def _format_attachments(self):
        return [DISCUSSION_INTRO_ACTIONS_ATTACHMENT]


class HelpMessage(Message):
    def __init__(self, topic_channel_id):
        super().__init__(
            text=self._format_text(topic_channel_id=topic_channel_id),
        )

    def _format_text(self, topic_channel_id):
        return dedent(f'''
            Strand helps you have discussions within your team.

            Start a discussion with `/strand post`, or close an ongoing discussion with `/strand close`.

            Read more about Strand at www.trystrand.com/teams

            Head over to <#{topic_channel_id}> to see all the ongoing discussions on your team!
        ''')


class SavedMessageAsTopicMessage(Message):
    def __init__(self, topic_channel_id):
        super().__init__(
            text=self._format_text(topic_channel_id=topic_channel_id),
        )

    def _format_text(self, topic_channel_id):
        return dedent(f'''
            The message you reacted to has been successfully saved. :boom:

            To save more topics, simply react to a post with :floppy_disk:!
        ''')
