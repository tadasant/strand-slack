from src.command.model.message.TopicMessage import TopicMessage


class ChannelMessage(TopicMessage):
    def __init__(self, original_poster_user_id, discussion_channel_id, title, tag_names):
        super().__init__(original_poster_user_id=original_poster_user_id, discussion_channel_id=discussion_channel_id,
                         title=title, tag_names=tag_names)

    def _format_text(self):
        return f'<@{self._original_poster_user_id}> just shared a topic with this channel. ' \
               f'Join the discussion :arrow_right: <#{self._discussion_channel_id}>'
