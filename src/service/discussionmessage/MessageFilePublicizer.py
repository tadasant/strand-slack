class MessageFilePublicizer:
    def __init__(self, discussion_message, slack_client_wrapper, slack_team_id):
        self.discussion_message = discussion_message
        self.slack_client_wrapper = slack_client_wrapper
        self.slack_team_id = slack_team_id

    def publicize_file(self):
        """Return a URL to a public file"""
        if self.discussion_message.file.public_url_shared:
            return self.discussion_message.file.permalink_public
        else:
            file_info = self.slack_client_wrapper.publicize_file(slack_team_id=self.slack_team_id,
                                                                 file_id=self.discussion_message.file.id)
        return file_info.get('permalink_public')
