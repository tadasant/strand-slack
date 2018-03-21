import json

from src.models.slack.elements.SlackMessage import SlackMessage
from src.models.slack.outgoing.attachments import EditMetadataButtonAttachment


class HelpSlackMessage(SlackMessage):
    def __init__(self):
        super().__init__(
            text=self._format_text(),
        )

    def _format_text(self):
        return 'Strand lets you save anything from Slack to your team’s shared knowledge-base. Make it easy for ' + \
               'you and your team to find important conversations by saving them from any channel or DM to Strand. ' + \
               'You can see what your team has saved so far right here: app.trystrand.com ' + \
               'Want to save something? Simply copy it and send it as a direct message to me in this window ' + \
               '- I\'ll figure out the rest.'


class PleaseInstallSlackMessage(SlackMessage):
    def __init__(self):
        super().__init__(
            text=self._format_text(),
        )

    def _format_text(self):
        return 'Someone on your team has installed the Strand app on this workspace. However, each ' + \
               'user must install it themselves to use it. Please visit the following site: ' + \
               'https://app.trystrand.com/install\n\n' + \
               'Haven’t heard of Strand? Strand helps teams save any information that is exchanged to a shared ' + \
               'knowledge-base. You can save anything from public channels, private channels, or DMs. By pooling ' + \
               'insights from the entire team, you’ll be able to make more informed decisions, spend less time ' + \
               'looking for them, and bother your colleagues less. Saving information is simple - just install the ' + \
               'app, and then send anything you want to share to me as a direct message.\n\n' + \
               'Take a look at what your team has saved at app.trystrand.com, or get started by installing the app.'


class MetadataUpdatedSlackMessage(SlackMessage):
    def __init__(self):
        super().__init__(
            text=self._format_text(),
        )

    def _format_text(self):
        return 'Your strand\'s metadata was successfully updated!'


class SavedStrandSlackMessage(SlackMessage):
    def __init__(self, strand_id):
        self.strand_id = strand_id

        self.text = self._format_text()
        self.attachments = self._format_attachments()
        super().__init__(text=self.text, attachments=self.attachments)

    def _format_text(self):
        return 'Your content has been saved to app.trystrand.com. If you did not create an account before, ' + \
               'check your email for instructions on how to register. To edit the title and tags of your ' + \
               'strand, click below.'

    def _format_attachments(self):
        return [json.loads(EditMetadataButtonAttachment(strand_id=self.strand_id).to_json())]


class WelcomeSlackMessage(SlackMessage):
    def __init__(self):
        super().__init__(
            text=self._format_text(),
        )

    def _format_text(self):
        return 'Successfully installed Strand! You can now save anything important to your team\'s shared ' + \
               'knowledge-base. Want to save something? Simply copy it and send it as a direct message to ' + \
               'me in this window - I\'ll figure out the rest.'
