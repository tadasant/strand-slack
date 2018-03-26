import re
import time

from src.services.Service import Service


class ConvertTextToGFMService(Service):
    """Given text, convert to Github Flavored Markdown"""

    def __init__(self, text, slack_team_id, slack_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper)
        self.text = text
        self.slack_team_id = slack_team_id

    def execute(self):
        """Return the converted markdown"""
        self.logger.debug(f'Converting text to GFM: {repr(self.text)}')

        # 1. Convert Bold text
        ghm = re.sub('\*(.*?)\*', lambda x: x.group().replace('*', '**'), self.text)

        # 2. No need to convert italics (_italics_), inline code (`code`), and multiline code(```code```)

        # 3. Convert Strikethrough
        ghm = re.sub('\~(.*?)\~', lambda x: x.group().replace('~', '~~'), ghm)

        # 4. Convert Links and Commands
        ghm = re.sub('<(.*?)>', self.convert_links_and_commands, ghm)

        # 5. Replace newline (\n) character with two newline chracters
        ghm = ghm.replace('\n', '\n\n')

        return ghm

    def convert_links_and_commands(self, matchgroup):
        matchtext = matchgroup.group(1)

        # 1. format content starting with #C as a channel link
        if matchtext.startswith('#C'):
            if '|' in matchtext:
                channel_name = matchtext.split('|')[1].strip()
            else:
                channel = self.slack_client_wrapper.get_channel_info(self.slack_team_id, matchtext[1:])
                channel_name = channel['name']
            return '#{}'.format(channel_name)

        # 2. format content starting with @U or @W as a user link
        if matchtext.startswith('@U') or matchtext.startswith('@W'):
            if '|' in matchtext:
                username = matchtext.split('|')[1].strip()
            else:
                user = self.slack_client_wrapper.get_user_info(self.slack_team_id, matchtext[1:])
                username = user.profile.display_name
            return '@{}'.format(username)

        # 3. format content starting with ! according to the rules for the special command.
        if matchtext.startswith('!'):
            if matchtext.startswith('!date'):
                timestamp = int(matchtext.split('^')[1])
                return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

        # 4. format URLs
        if '|' in matchtext:
            link_url = matchtext.split('|')[0]
            link_name = matchtext.split('|')[1]
            return '[{}]({})'.format(link_name, link_url)
        else:
            return matchtext
