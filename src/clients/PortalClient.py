# TODO [CCS-26] Add authentication
import requests


class PortalClient:
    def __init__(self, host, endpoint):
        self.url = f'{host}{endpoint}'

    def query(self, operation_definition):
        full_definition = f'query {operation_definition}'
        response = requests.post(url=self.url, data=full_definition)
        if response.status_code != 200:
            raise PortalClientException('Query failed.', response)
        return response.json()['data']


class PortalClientException(Exception):
    def __init__(self, message, response):
        self.message = message
        self.response = response

    def __str__(self):
        return f'PortalClientException: {message}\nresponse: repr(self.response)'