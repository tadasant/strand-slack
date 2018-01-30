import json
from http import HTTPStatus
from urllib.parse import urlencode

import pytest
from flask import url_for

from src.command.messages.post_topic_dialog import POST_TOPIC_DIALOG
from src.config import config
from src.domain.models.portal.SlackAgent import SlackAgent
from src.domain.models.portal.SlackAgentStatus import SlackAgentStatus
from src.domain.models.portal.SlackApplicationInstallation import SlackApplicationInstallation
from src.domain.models.portal.SlackTeam import SlackTeam
from src.domain.models.portal.SlackUser import SlackUser
from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.factories.slackfactories import InteractiveComponentRequestFactory, SubmissionFactory
from tests.utils import wait_until


@pytest.mark.usefixtures('client_class')  # pytest-flask's client_class adds self.client
class TestStartDiscussion:
    # For assertions
    fake_tags = [str(PrimitiveFaker('word')), str(PrimitiveFaker('word'))]
    fake_interactive_component_request = InteractiveComponentRequestFactory.create(
        submission=SubmissionFactory.create(tags=', '.join(fake_tags)),
        callback_id=POST_TOPIC_DIALOG.callback_id,
        type='dialog_submission'
    )

    # For setup
    target_endpoint = 'slack.interactivecomponentresource'
    default_payload = {
        "type": fake_interactive_component_request.type,
        "callback_id": fake_interactive_component_request.callback_id,
        "submission": {
            "title": fake_interactive_component_request.submission.title,
            "description": fake_interactive_component_request.submission.description,
            "tags": fake_interactive_component_request.submission.tags
        },
        "team": {
            "id": fake_interactive_component_request.team.id,
            "domain": "solutionloft"
        },
        "channel": {
            "id": "D8YS0A9D1",
            "name": "directmessage"
        },
        "user": {
            "id": fake_interactive_component_request.user.id,
            "name": "tadas"
        },
        "action_ts": "1517014983.191305",
        "token": config['SLACK_VERIFICATION_TOKEN'],
    }
    default_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def test_post_valid_unauthenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)
        payload = self.default_payload.copy()
        payload['token'] = 'unverified-token'
        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(payload)}))
        assert response.json['error'] == 'Invalid slack verification token'

    def test_post_valid_authenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(self.default_payload)}))
        assert HTTPStatus.OK == response.status_code

    def test_post_with_existing_user(self, portal_client, slack_agent_repository, mocker):
        mocker.spy(portal_client, 'mutate')
        target_url = url_for(endpoint=self.target_endpoint)
        fake_topic_id = str(PrimitiveFaker('ean8'))

        # Need team's slack agent to be present in memory
        slack_agent_repository.add_slack_agent(slack_agent=SlackAgent(
            status=SlackAgentStatus.ACTIVE,
            slack_team=SlackTeam(id=self.fake_interactive_component_request.team.id),
            slack_application_installation=SlackApplicationInstallation(access_token='doesnt matter',
                                                                        installer=SlackUser(id='doesnt matter'),
                                                                        bot_access_token='doesnt matter'))
        )

        # Set up successful topic creation
        portal_client.set_next_response({
            'data': {
                'createTopicFromSlack': {
                    'topic': {
                        'id': fake_topic_id,
                        'title': self.fake_interactive_component_request.submission.title,
                        'description': self.fake_interactive_component_request.submission.description,
                        'tags': [
                            {'name': self.fake_tags[0].lower()},
                            {'name': self.fake_tags[1].lower()}
                        ],
                    },
                }
            }
        })

        # Set up successful discussion creation
        portal_client.set_next_response({
            'data': {
                'createDiscussionFromSlack': [{
                    'discussion': {
                        'id': str(PrimitiveFaker('ean8')),
                        'name': str(PrimitiveFaker('word'))
                    },
                }]
            }
        })

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(self.default_payload)}))
        assert HTTPStatus.OK == response.status_code

        # topic creation assertions
        outcome = wait_until(condition=lambda: portal_client.mutate.call_count >= 1)
        assert outcome, 'PortalClient mutate was never called'
        assert 'createTopicFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']

        # discussion creation assertions
        outcome = wait_until(condition=lambda: portal_client.mutate.call_count == 2)
        assert outcome, 'PortalClient mutate not called twice'
        assert 'createDiscussionFromSlack' in portal_client.mutate.call_args_list[1][1]['operation_definition']
        assert fake_topic_id in portal_client.mutate.call_args_list[1][1]['operation_definition']

    def test_post_with_nonexisting_user(self, portal_client, slack_client_class, slack_agent_repository, mocker):
        mocker.spy(portal_client, 'mutate')
        mocker.spy(slack_client_class, 'api_call')
        target_url = url_for(endpoint=self.target_endpoint)

        # Need team's slack agent to be present in memory
        slack_agent_repository.add_slack_agent(slack_agent=SlackAgent(
            status=SlackAgentStatus.ACTIVE,
            slack_team=SlackTeam(id=self.fake_interactive_component_request.team.id),
            slack_application_installation=SlackApplicationInstallation(access_token='doesnt matter',
                                                                        installer=SlackUser(id='doesnt matter'),
                                                                        bot_access_token='doesnt matter'))
        )

        # Set up a failed call & successful portal/user creation
        portal_client.set_next_response(None)
        portal_client.set_next_response({
            'data': {
                'createUserAndTopicFromSlack': [{
                    'topic': {
                        'id': str(PrimitiveFaker('ean8')),
                        'title': self.fake_interactive_component_request.submission.title,
                        'description': self.fake_interactive_component_request.submission.description,
                        'tags': [
                            {'name': self.fake_tags[0].lower()},
                            {'name': self.fake_tags[1].lower()}
                        ],
                    },
                }]
            }
        })

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(self.default_payload)}))
        assert HTTPStatus.OK == response.status_code
        outcome = wait_until(condition=lambda: portal_client.mutate.call_count == 2)
        assert outcome, 'PortalClient mutate was not called twice'
        assert slack_client_class.api_call.call_args[1]['method'] == 'users.info'
        assert slack_client_class.api_call.call_args[1]['user'] == self.fake_interactive_component_request.user.id
        # TODO brittle test; later assert that it did the right thing (esp. w/ tags) w/ the resulting Topic
