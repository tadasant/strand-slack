from textwrap import dedent

from src.commands.model.message.Message import Message


class HelpMessage(Message):
    def __init__(self):
        super().__init__(
            text=self._format_text(),
        )

    def _format_text(self):
        return dedent(f'''
            Strand helps you have share bookmarks with your team.

            Read more about Strand at www.trystrand.com/teams
        ''')
