# TODO [CCS-61] test this / effectively treat it as an independent package (or use an existing graphql client?)
import requests

"""
This client library returns the results of a GraphQL query on {host}{endpoint}.

If the GraphQL operation fails due to an HTTP error, will throw a PortalClientException.

If there are GraphQL errors for the operation, will return the standard {'errors': [...]} GraphQL response format.
"""


class PortalClient:
    def __init__(self, host, endpoint):
        self.url = f'{host}{endpoint}'

    def query(self, operation_definition):
        full_definition = f'query {operation_definition}'
        response = requests.post(url=self.url, data={'query': full_definition})
        if response.status_code != 200:
            raise PortalClientException('Query failed.', response)
        return response.json()

    def mutate(self, operation_definition):
        full_definition = f'mutation {operation_definition}'
        response = requests.post(url=self.url, data={'query': full_definition})
        if response.status_code != 200:
            raise PortalClientException('Mutation failed.', response)
        return response.json()


class PortalClientException(Exception):
    def __init__(self, message, response):
        self.message = message
        self.response = response

    def __str__(self):
        return f'{self.message}\n\tStatus: {self.response.status_code}\n\t' \
               f'Reason: {self.response.reason}\n\tText: {self.response.text}'
