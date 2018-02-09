from collections import namedtuple

# TODO [CCS-104] Move this to message_models.py & messages.py

UpdateTopicChannelDmType = namedtuple('UpdateTopicChannelDmType', 'attachment_generator')


def _generate_attachment(topic_channel_id):
    return {
        "fallback": "Failed to load message.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "text": f'You\'ve set the discussion topics channel to be <#{topic_channel_id}>!'
    }


UPDATE_TOPIC_CHANNEL_DM = UpdateTopicChannelDmType(
    attachment_generator=_generate_attachment
)
