from src.command.model.message.message_models import TopicShareMessage

# TODO [SLA-104] Move this to message_models.py & messages.py


class TopicChannelTopicShareMessage(TopicShareMessage):
    def __init__(self, original_poster_user_id, discussion_channel_id, title, tag_names):
        super().__init__(original_poster_user_id=original_poster_user_id, discussion_channel_id=discussion_channel_id,
                         title=title, tag_names=tag_names)
