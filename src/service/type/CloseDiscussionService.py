import re
from threading import Thread

from src.command.CloseChannelCommand import CloseChannelCommand
from src.command.CloseDiscussionCommand import CloseDiscussionCommand
from src.command.InformUserUnauthorizedCommand import InformUserUnauthorizedCommand
from src.command.UpdateQueueCommand import UpdateQueueCommand
from src.domain.repositories.SlackAgentRepository import slack_agent_repository
from src.service.Service import Service


class CloseDiscussionService(Service):
    """
        Closes the discussion

        Actions:
        * Checks if slack user is OP or admin (will refactor out to validator in SLA-81 TODO)

        Outputs:
        * Request to CoreApi (close discussion)
    """

    def __init__(self, slack_client_wrapper, core_api_client_wrapper, slack_team_id, slack_user_id, slack_channel_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper, core_api_client_wrapper=core_api_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id

    def execute(self):
        if self._is_discussion_channel():
            if self._user_is_authorized():
                core_api_command = CloseDiscussionCommand(core_api_client_wrapper=self.core_api_client_wrapper,
                                                          slack_channel_id=self.slack_channel_id,
                                                          slack_team_id=self.slack_team_id,
                                                          slack_user_id=self.slack_user_id)
                Thread(target=core_api_command.execute, daemon=True).start()
                close_channel_command = CloseChannelCommand(slack_client_wrapper=self.slack_client_wrapper,
                                                            slack_channel_id=self.slack_channel_id,
                                                            slack_team_id=self.slack_team_id,
                                                            slack_user_id=self.slack_user_id)
                Thread(target=close_channel_command.execute, daemon=True).start()
                topic_slack_channel_id = slack_agent_repository.get_topic_channel_id(
                    slack_team_id=self.slack_team_id
                )
                update_queue_command = UpdateQueueCommand(slack_client_wrapper=self.slack_client_wrapper,
                                                          topic_slack_channel_id=topic_slack_channel_id,
                                                          discussion_slack_channel_id=self.slack_channel_id,
                                                          slack_team_id=self.slack_team_id)
                Thread(target=update_queue_command.execute, daemon=True).start()
            else:
                inform_user_unauthorized_command = InformUserUnauthorizedCommand(
                    slack_client_wrapper=self.slack_client_wrapper,
                    slack_channel_id=self.slack_channel_id,
                    slack_team_id=self.slack_team_id,
                    slack_user_id=self.slack_user_id
                )
                Thread(target=inform_user_unauthorized_command.execute, daemon=True).start()

    def _is_discussion_channel(self):
        # TODO [SLA-81] This check should happen via db in validator
        calling_channel_info = self.slack_client_wrapper.get_channel_info(slack_team_id=self.slack_team_id,
                                                                          slack_channel_id=self.slack_channel_id)
        calling_channel_name = calling_channel_info['name']
        return re.fullmatch(pattern=r'discussion-(\d+)', string=calling_channel_name) is not None

    def _user_is_authorized(self):
        # TODO [SLA-81] This check should happen via db in validator
        return self._user_is_slack_admin() or self._user_is_original_poster()

    def _user_is_slack_admin(self):
        user_info = self.slack_client_wrapper.get_user_info(slack_team_id=self.slack_team_id,
                                                            slack_user_id=self.slack_user_id)
        return user_info['is_admin']

    def _user_is_original_poster(self):
        intro_message = self.slack_client_wrapper.get_discussion_channel_intro_message(
            slack_team_id=self.slack_team_id,
            discussion_channel_id=self.slack_channel_id
        )
        if not intro_message or 'OP' not in intro_message.text:
            self.logger.warning('Couldn\'t find the actual intro message for authorizing OP. Assuming OP.')
            return True
        return self.slack_user_id in intro_message.text
