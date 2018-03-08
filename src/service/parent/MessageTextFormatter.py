import re

import emoji
import markdown2


class MessageTextFormatter:
    def __init__(self, discussion_message):
        self.discussion_message = discussion_message

    def format_text(self):
        text = self.discussion_message.text
        text = text.replace('<!channel>', '@channel')
        text = self._slack_to_accepted_emoji(text)

        # Handle '<@U0BM1CGQY|calvinchanubc> has joined the channel'
        text = re.sub(r'<@U\d\w+\|[A-Za-z0-9.-_]+>', self._sub_annotated_mention, text)
        # Handle '<@U0BM1CGQY>'
        text = re.sub(r'<@U\d\w+>', self._sub_mention, text)

        # Handle links
        text = re.sub(r'<(https|http|mailto):[A-Za-z0-9_\.\-\/\|\?\,\=\#\:\@]+>', self._sub_hyperlink, text)
        # Handle hashtags (that are meant to be hashtags and not headings)
        text = re.sub(r'(^| )#[A-Za-z0-9\.\-\_]+( |$)', self._sub_hashtag, text)
        # Handle channel references
        text = re.sub(r'<#C0\w+>', self._sub_channel_ref, text)
        # Handle italics (convert * * to ** **)
        text = re.sub(r'(^| )\*[A-Za-z0-9\-._ ]+\*( |$)', self._sub_bold, text)
        # Handle italics (convert _ _ to * *)
        text = re.sub(r'(^| )_[A-Za-z0-9\-._ ]+_( |$)', self._sub_italics, text)
        # Escape any remaining hash characters to save them from being turned into headers by markdown2
        text = text.replace('#', '\\#')

        text = markdown2.markdown(
            text=text,
            extras=['cuddled-lists', 'code-friendly', 'fenced-code-blocks', 'pyshell']
        ).strip()

        # markdown2 likes to wrap everything in <p> tags
        if text.startswith('<p>') and text.endswith('</p>'):
            text = text[3:-4]

        # Special handling cases for lists
        text = text.replace('\n\n<ul>', '<ul>')
        text = text.replace('\n<li>', '<li>')
        # Indiscriminately replace everything else
        text = text.replace('\n', '<br />')
        # Introduce unicode emoji
        text = emoji.emojize(text, use_aliases=True)

        if self.discussion_message.file_url:
            text = re.sub('(https):(.*?)\|', self.discussion_message.file_url + '|', text)
        return text

    @staticmethod
    def _slack_to_accepted_emoji(message):
        # https://github.com/Ranks/emojione/issues/114
        message = message.replace(':simple_smile:', ':slightly_smiling_face:')
        return message

    @staticmethod
    def _sub_mention(matchobj):
        # TODO query users in our DB
        # return '@{}'.format(self._channel_members[matchobj.group(0)[2:-1]])
        return '@user'

    @staticmethod
    def _sub_annotated_mention(matchobj):
        return '@{}'.format((matchobj.group(0)[2:-1]).split('|')[1])

    @staticmethod
    def _sub_hyperlink(matchobj):
        compound = matchobj.group(0)[1:-1]
        if len(compound.split('|')) == 2:
            url, title = compound.split('|')
        else:
            url, title = compound, compound
        result = '[{title}]({url})'.format(url=url, title=title)
        return result

    @staticmethod
    def _sub_hashtag(matchobj):
        text = matchobj.group(0)

        starting_space = ' ' if text[0] == ' ' else ''
        ending_space = ' ' if text[-1] == ' ' else ''

        return '{}*{}*{}'.format(starting_space, text.strip(), ending_space)

    def _sub_channel_ref(self):
        channel_id = self.discussion_message.channel_id
        return '*#{}*'.format(channel_id)

    @staticmethod
    def __em_strong(matchobj, format='em'):
        if format not in ('em', 'strong'):
            raise ValueError
        chars = '*' if format == 'em' else '**'

        text = matchobj.group(0)
        starting_space = ' ' if text[0] == ' ' else ''
        ending_space = ' ' if text[-1] == ' ' else ''
        return '{}{}{}{}{}'.format(starting_space, chars, matchobj.group(0).strip()[1:-1], chars, ending_space)

    def _sub_italics(self, matchobj):
        return self.__em_strong(matchobj, 'em')

    def _sub_bold(self, matchobj):
        return self.__em_strong(matchobj, 'strong')
