from collections import namedtuple

# TODO [SLA-104] Move this to message_models.py & messages.py

PostTopicDialogType = namedtuple('PostTopicDialogType', 'callback_id value')

_post_topic_dialog_callback_id = 'post_topic_dialog'
POST_TOPIC_DIALOG = PostTopicDialogType(
    callback_id=_post_topic_dialog_callback_id,
    value={
        'title': 'Post Topic',
        'submit_label': 'Discuss',
        'callback_id': _post_topic_dialog_callback_id,
        'elements': [
            {
                'label': 'Title',
                'name': 'title',
                'type': 'text',
            },
            {
                'label': 'Description',
                'name': 'description',
                'type': 'textarea',
                'max_length': 500,
            },
            {
                'label': 'Tags',
                'name': 'tags',
                'type': 'text',
                'hint': 'Please separate with commas. E.g. "Python, React, MySQL"',
            }
        ]
    }
)

POST_TOPIC_DIALOG_WITH_CHANNEL_OPTION = PostTopicDialogType(
    callback_id=_post_topic_dialog_callback_id,
    value={
        'title': 'Post Topic',
        'submit_label': 'Discuss',
        'callback_id': _post_topic_dialog_callback_id,
        'elements': [
            {
                'label': 'Title',
                'name': 'title',
                'type': 'text',
            },
            {
                'label': 'Description',
                'name': 'description',
                'type': 'textarea',
                'max_length': 500,
            },
            {
                'label': 'Tags',
                'name': 'tags',
                'type': 'text',
                'hint': 'Please separate with commas. E.g. "Python, React, MySQL"',
            },
            {
                'label': 'Share with channel?',
                'name': 'share_with_current_channel',
                'type': 'select',
                'value': 'false',
                'options': [
                    {
                        'label': 'Yes',
                        'value': 'true'
                    },
                    {
                        'label': 'No',
                        'value': 'false'
                    }
                ],
                'hint': 'The topic will be shared in this channel.'
            }
        ]
    }
)
