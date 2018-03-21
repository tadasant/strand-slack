from src.models.slack.elements.SlackAction import SlackAction


class EditMetadataButton(SlackAction):
    def __init__(self, value=''):
        super().__init__(
            name='edit_metadata',
            text='Edit Metadata',
            type='button',
            value=value
        )
