from textwrap import dedent

from src.models.slack.elements.SlackMessage import SlackMessage


class SlackMessageHelp(SlackMessage):
    def __init__(self):
        super().__init__(
            text=self._format_text(),
        )

    def _format_text(self):
        return dedent(f'''
            Strand lets you save anything from Slack to your team’s shared knowledge-base. Make it easy for you and\
            your team to find important conversations by saving them from any channel or DM to Strand. You can see\
            what your team has saved so far right here: app.trystrand.com

            Want to save something? Simply copy it and send it as a direct message to me in this window - I’ll figure\
            out the rest.
        ''')


class SlackMessagePleaseInstall(SlackMessage):
    def __init__(self):
        super().__init__(
            text=self._format_text(),
        )

    def _format_text(self):
        return dedent(f'''
            Someone on your team has approved Strand. To use it, install it yourself here: www.trystrand.com/teams

            Haven’t heard of Strand? Strand helps teams save any information that is exchanged to a shared\
            knowledge-base. You can save anything from public channels, private channels, or DMs. By pooling insights\
            from the entire team, you’ll be able to make more informed decisions, spend less time looking for them,\
            and bother your colleagues less. Saving information is simple - just install the app, and then send\
            anything you want to share to me as a direct message.

            Take a look at what your team has saved at app.trystrand.com, or get started by installing the app.
        ''')
