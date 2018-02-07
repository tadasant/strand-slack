import time


class TopicChannelMessage:
    def __init__(self, original_poster_user_id, discussion_channel_id, team_domain, title, tag_names):
        self._original_poster_user_id = original_poster_user_id
        self._discussion_channel_id = discussion_channel_id
        self._team_domain = team_domain
        self._title = title
        self._tag_names = [x.lower() for x in tag_names]
        self._ts = time.time()

        self.text = self._format_text()
        self.attachments = self._format_attachments()

    def _format_text(self):
        return f'New topic posted. Join the discussion :arrow_right: <#{self._discussion_channel_id}>'

    def _format_attachments(self):
        return [self._format_title_attachment(), self._format_tag_attachment()]

    def _format_title_attachment(self):
        return {
            'fallback': f'*Title*: {self._title}',
            'color': '#32424a',
            'author_name': 'Posted by <@adi>',
            'author_link': f'https://{self._team_domain}.slack.com/team/{self._original_poster_user_id}',
            'title': self._title,
            'title_link': f'https://{self._team_domain}.slack.com/messages/{self._discussion_channel_id}'
        }

    def _format_tag_attachment(self):
        return {
            'fallback': f'*Tags*: {", ".join(self._tag_names)}',
            'color': '#32424a',
            'author_name': ", ".join(self._tag_names),
            'fields': [],
            'footer': 'CodeClippy',
            'footer_icon': 'https://i.imgur.com/kPCJwwl.png',
            'ts': self._ts
        }
