from collections import namedtuple

InitialOnboardingDmType = namedtuple('OnboardingDmType', 'callback_id action_id text attachment')

_initial_onboarding_dm_callback_id = 'onboarding_dm'
_initial_onboarding_dm_action_id = 'discuss_channel_list'
INITIAL_ONBOARDING_DM = InitialOnboardingDmType(
    callback_id=_initial_onboarding_dm_callback_id,
    action_id=_initial_onboarding_dm_action_id,
    text="Hey there! I'm your CodeClippy agent :sleuth_or_spy:\n\nWhat channel should I use for "
         "showing discussion topics?",
    attachment={
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": _initial_onboarding_dm_callback_id,
        "actions": [
            {
                "name": _initial_onboarding_dm_action_id,
                "text": "What channel should I use for showing discussion topics?",
                "type": "select",
                "data_source": "channels"
            }
        ]
    }
)
