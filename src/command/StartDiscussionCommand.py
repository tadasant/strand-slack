from src.command.Command import Command
from src.domain.models.exceptions import WrapperException


class StartDiscussionCommand(Command):
    def __init__(self, slack_client_wrapper, portal_client_wrapper, slack_team_id):
        super().__init__(slack_team_id=slack_team_id, slack_client_wrapper=slack_client_wrapper,
                         portal_client_wrapper=portal_client_wrapper)

    def execute(self):
        self.logger.info(f'Executing StartDiscussionCommand for {self.slack_team_id}')
        try:
            self._create_topic()
            # TODO creating a new discussion [next ticket]
        except WrapperException:
            # TODO send DM to user informing them to contact support
            pass
        # TODO send DM to user informing them of the creation of their session

    def _create_topic(self):
        # TODO [CCS-60] move tag parsing to useful validation
        # parse the tags
        # pass them onto portal
        # TODO [CCS-15] caching user info to avoid relying on error
        # if portal errors due to lack of user info..
        #   fetch user info
        #   re-send the info to portal w/ addition of user info
        pass
