from src.command.action.actions import POST_NEW_TOPIC_BUTTON
from src.command.attachment.Attachment import Attachment


class TopicChannelActionsAttachment(Attachment):
    def __init__(self):
        super().__init__(
            fallback=f'Can\'t display the attachment, please use `/codeclippy post`',
            callback_id='post_new_topic',
            color='#3AA3E3',
            attachment_type='default',
            actions=[POST_NEW_TOPIC_BUTTON]
        )
