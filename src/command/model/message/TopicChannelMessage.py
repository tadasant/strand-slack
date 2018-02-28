import time

# TODO [SLA-104] Move this to message_models.py & messages.py


class TopicChannelMessage:
    def __init__(self, original_poster_user_id, discussion_channel_id, title, tag_names):
        self._original_poster_user_id = original_poster_user_id
        self._discussion_channel_id = discussion_channel_id
        self._title = title
        self._tag_names = [x.lower() for x in tag_names]
        self._ts = time.time()

        self.text = self._format_text()
        self.attachments = self._format_attachments()

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
