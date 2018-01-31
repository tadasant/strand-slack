from collections import namedtuple

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
