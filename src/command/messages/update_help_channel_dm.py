from collections import namedtuple

UpdateHelpChannelDmType = namedtuple('UpdateHelpChannelDmType', 'attachment_generator')


def _generate_attachment(help_channel_id):
    return {
        "fallback": "Failed to load message.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "text": f'You\'ve set the help channel to be <#{help_channel_id}>!'
    }


UPDATE_HELP_CHANNEL_DM = UpdateHelpChannelDmType(
    attachment_generator=_generate_attachment
)
