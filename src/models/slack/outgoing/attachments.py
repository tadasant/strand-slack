from src.models.slack.elements.SlackAttachment import SlackAttachment
from src.models.slack.outgoing.actions import EditMetadataButton


class EditMetadataButtonAttachment(SlackAttachment):
    def __init__(self, strand_id):
        super().__init__(
            callback_id='edit_metadata_button',
            color='#3AA3E3',
            attachment_type='default',
            actions=[EditMetadataButton(value=strand_id)]
        )
