class MessageFilePublicizer:
    def __init__(self, event, slack_client_wrapper, slack_team_id):
        self.event = event
        self.slack_client_wrapper = slack_client_wrapper
        self.slack_team_id = slack_team_id

    def publicize_file(self):
        """Return a URL to a public file"""
        if self.event.file.public_url_shared:
            return self.event.file.permalink_public
        else:
            file_info = self.slack_client_wrapper.publicize_file(slack_team_id=self.slack_team_id,
                                                                 file_id=self.event.file.id)
        return file_info.get('permalink_public')
