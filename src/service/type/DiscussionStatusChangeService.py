from threading import Thread

from src.command.CloseChannelCommand import CloseChannelCommand
from src.command.MarkDiscussionPendingClosed import MarkDiscussionPendingClosed
from src.command.UpdateQueueCommand import UpdateQueueCommand
from src.domain.models.coreapi.Discussion import DiscussionStatus
from src.domain.repositories.SlackAgentRepository import slack_agent_repository
from src.service.Service import Service


class DiscussionStatusChangeService(Service):
    """
        Actions:
        * If STALE, sends a message to the channel informing participants & inform core_api we did it
        * If CLOSED, sends close message, archives channel, and updates topic list

        Outputs:
        * If STALE, pending_closed call to core_api
    """

    def __init__(self, slack_client_wrapper, core_api_client_wrapper, slack_team_id, slack_channel_id,
                 discussion_status):
        super().__init__(slack_client_wrapper=slack_client_wrapper, core_api_client_wrapper=core_api_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_channel_id = slack_channel_id
        self.discussion_status = discussion_status

    def execute(self):
        if self.discussion_status == DiscussionStatus.CLOSED:
            slack_bot_user_id = slack_agent_repository.get_slack_bot_user_id(slack_team_id=self.slack_team_id)
            close_channel_command = CloseChannelCommand(slack_client_wrapper=self.slack_client_wrapper,
                                                        slack_channel_id=self.slack_channel_id,
                                                        slack_team_id=self.slack_team_id,
                                                        slack_user_id=slack_bot_user_id)
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
            command = MarkDiscussionPendingClosed(slack_client_wrapper=self.slack_client_wrapper,
                                                  core_api_client_wrapper=self.core_api_client_wrapper,
                                                  slack_team_id=self.slack_team_id,
                                                  slack_channel_id=self.slack_channel_id)
            Thread(target=command.execute, daemon=True).start()
