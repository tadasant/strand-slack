from src.service.Service import Service


class DiscussionStatusChangeService(Service):
    """
        Actions:
        * If STALE, sends a message to the channel informing participants & inform portal we did it
        * If CLOSED, sends close message, archives channel, and updates topic list

        Outputs:
        * If STALE, pending_closed call to portal
    """

    def __init__(self, slack_client_wrapper, portal_client_wrapper, slack_team_id, slack_channel_id, discussion_status):
        super().__init__(slack_client_wrapper=slack_client_wrapper, portal_client_wrapper=portal_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_channel_id = slack_channel_id
        self.discussion_status = discussion_status

    def execute(self):
        pass
        # * If CLOSED, sends close message, archives channel, and updates topic list
        # TODO next ticket * If STALE, sends a message to the channel informing participants & inform portal we did it
