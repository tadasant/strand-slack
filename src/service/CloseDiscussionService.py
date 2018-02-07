import re

from src.service.Service import Service


class CloseDiscussionService(Service):
    """
        Closes the discussion

        Actions:
        * Checks if slack user is OP or admin (will refactor out to validator in CCS-81 TODO)

        Outputs:
        * Request to Portal (close discussion)
    """

    def __init__(self, slack_client_wrapper, portal_client_wrapper, slack_team_id, slack_user_id, slack_channel_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper, portal_client_wrapper=portal_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id

    def execute(self):
        if self._is_discussion_channel():
            if self._user_is_authorized():
                # perform closing command(s)
                pass

    def _is_discussion_channel(self):
        # TODO [CCS-81] This check should happen via db in validator
        calling_channel_info = self.slack_client_wrapper.get_channel_info(slack_team_id=self.slack_team_id,
                                                                          slack_channel_id=self.slack_channel_id)
        calling_channel_name = calling_channel_info['name']
        return re.fullmatch(pattern=r'discussion-(\d+)', string=calling_channel_name) is not None

    def _user_is_authorized(self):
        # TODO [CCS-81] This check should happen via db in validator
        return self._user_is_slack_admin() or self._user_is_original_poster()

    def _user_is_slack_admin(self):
        user_info = self.slack_client_wrapper.get_user_info(slack_team_id=self.slack_team_id,
                                                            slack_user_id=self.slack_user_id)
        return user_info['is_admin']

    def _user_is_original_poster(self):
        intro_message_info = self.slack_client_wrapper.get_first_channel_message(slack_team_id=self.slack_team_id,
                                                                                 slack_channel_id=self.slack_channel_id)
        if 'OP' not in intro_message_info['text']:
            self.logger.warning('Couldn\'t find the actual intro message for authorizing OP. Assuming OP.')
            return True
        return self.slack_user_id in intro_message_info['text']
