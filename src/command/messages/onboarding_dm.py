from collections import namedtuple

OnboardingDmType = namedtuple('OnboardingDmType', 'callback_id text attachment')

_onboarding_dm_callback_id = 'onboarding_dm'
ONBOARDING_DM = OnboardingDmType(
    callback_id=_onboarding_dm_callback_id,
    text="Hey there! I'm your CodeClippy agent :sleuth_or_spy:\n\nWhat channel should I use for" \
         "showing help requests?",
    attachment={
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": _onboarding_dm_callback_id,
        "actions": [
            {
                "name": "help_channel_list",
                "text": "What channel should I use for showing help requests?",
                "type": "select",
                "data_source": "channels"
            }
        ]
    }
)
