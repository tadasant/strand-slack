from src.models.slack.elements.SlackDialog import SlackDialog
from src.models.slack.elements.SlackElement import SlackElement


class EditMetadataDialog(SlackDialog):
    callback_id_prefix = 'edit_metadata'

    def __init__(self, strand_id):
        super().__init__(
            title='Edit Metadata',
            submit_label='Save',
            callback_id=f'{self.callback_id_prefix}-{strand_id}',
            elements=self._generate_elements()
        )

    @staticmethod
    def _generate_elements():
        return [
            SlackElement(label='Title', name='title', type='text'),
            SlackElement(label='Tags', name='tags', type='text',
                         hint='Please separate with commas. E.g. "Python, React, MySQL"')
        ]
