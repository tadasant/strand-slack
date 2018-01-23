class TestPortalClient:
    def __init__(self, **kwargs):
        self.next_response = None
        pass

    # UTILITIES

    def set_next_response(self, response):
        self.next_response = response

    def clear_response(self):
        self.next_response = None

    # MOCKS

    def query(self, operation_definition):
        if self.next_response:
            result = self.next_response
            self.next_response = None
            return result
        elif 'slackTeamInstallations' in operation_definition:
            return {'slackTeamInstallations': []}
        return None
