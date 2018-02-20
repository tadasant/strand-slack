from src.command.model.action.actions import POST_NEW_TOPIC_BUTTON, CLOSE_DISCUSSION_BUTTON, \
    POST_NEW_TOPIC_BUTTON_WITH_CONFIRM
from src.command.model.attachment.Attachment import Attachment


class TopicChannelIntroActionsAttachment(Attachment):
    def __init__(self):
        super().__init__(
            fallback=f'Can\'t display the attachment, please use `/strand post`',
            callback_id='topic_channel_intro_attachment',
            color='#3AA3E3',
            attachment_type='default',
            actions=[POST_NEW_TOPIC_BUTTON]
        )


class DiscussionIntroActionsAttachment(Attachment):
    def __init__(self):
        super().__init__(
            callback_id='discussion_intro_attachment',
            color='#3AA3E3',
            attachment_type='default',
            actions=[CLOSE_DISCUSSION_BUTTON, POST_NEW_TOPIC_BUTTON_WITH_CONFIRM]
        )
