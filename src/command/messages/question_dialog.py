from collections import namedtuple

QuestionDialogType = namedtuple('QuestionDialogType', 'callback_id value')


def _generate_attachment(help_channel_id):
    return {
        "fallback": "Failed to load message.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "text": f'You\'ve set the help channel to be <#{help_channel_id}>!'
    }


_question_dialog_callback_id = 'question_dialog'
QUESTION_DIALOG = QuestionDialogType(
    callback_id=_question_dialog_callback_id,
    value={
        'label': 'Ask a Question',
        'submit_label': 'Submit',
        'callback_id': _question_dialog_callback_id,
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
