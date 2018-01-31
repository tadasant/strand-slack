from collections import namedtuple

UpdateDiscussChannelDmType = namedtuple('UpdateDiscussChannelDmType', 'attachment_generator')


def _generate_attachment(discuss_channel_id):
    return {
        "fallback": "Failed to load message.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "text": f'You\'ve set the discussion topics channel to be <#{discuss_channel_id}>!'
    }


UPDATE_DISCUSS_CHANNEL_DM = UpdateDiscussChannelDmType(
    attachment_generator=_generate_attachment
)
