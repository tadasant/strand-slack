import json

ONBOARDING_DM = {
    'callback_id': 'onboarding_dm',
    'text': "Hey there! I'm your CodeClippy agent :sleuth_or_spy:\n\nWhat channel "
            "should I use for showing help requests?",
}

ONBOARDING_DM['attachment'] = {
    "fallback": "Upgrade your Slack client to use messages like these.",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "callback_id": ONBOARDING_DM['callback_id'],
    "actions": [
        {
            "name": "help_channel_list",
            "text": "What channel should I use for showing help requests?",
            "type": "select",
            "data_source": "channels"
        }
    ]
}
