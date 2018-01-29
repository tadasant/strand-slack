from collections import namedtuple

PostTopicDialogType = namedtuple('PostTopicDialogType', 'callback_id value')


def _generate_attachment(help_channel_id):
    return {
        "fallback": "Failed to load message.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "text": f'You\'ve set the help channel to be <#{help_channel_id}>!'
    }


_post_topic_dialog_callback_id = 'post_topic_dialog'
POST_TOPIC_DIALOG = PostTopicDialogType(
    callback_id=_post_topic_dialog_callback_id,
    value={
        'label': 'Post Topic',
        'submit_label': 'Start Discussion',
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
