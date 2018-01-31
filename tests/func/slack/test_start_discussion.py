import json
from http import HTTPStatus
from urllib.parse import urlencode

from flask import url_for

from src.command.messages.post_topic_dialog import POST_TOPIC_DIALOG
from src.config import config
from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.factories.slackfactories import InteractiveComponentRequestFactory, SubmissionFactory
from tests.func.slack.TestSlackFunction import TestSlackFunction
from tests.utils import wait_until


class TestStartDiscussion(TestSlackFunction):
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

    def test_post_with_existing_user(self, portal_client, slack_agent_repository, slack_client_class, mocker):
        mocker.spy(portal_client, 'mutate')
        mocker.spy(slack_client_class, 'api_call')
        target_url = url_for(endpoint=self.target_endpoint)
        fake_topic_id = str(PrimitiveFaker('random_int'))
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_interactive_component_request.team.id)
        self._queue_portal_topic_creation(portal_client=portal_client, topic_id=fake_topic_id)
        self._queue_portal_discussion_creation(portal_client=portal_client)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(self.default_payload)}))

        def wait_condition():
            return portal_client.mutate.call_count == 2 and slack_client_class.api_call.call_count >= 5
        outcome = wait_until(condition=wait_condition)
        assert outcome, 'Expected portal_client to have 2 calls, and slack_client to have 5+'

        assert HTTPStatus.OK == response.status_code
        assert 'createTopicFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert 'createDiscussionFromSlack' in portal_client.mutate.call_args_list[1][1]['operation_definition']
        assert fake_topic_id in portal_client.mutate.call_args_list[1][1]['operation_definition']
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {
                    'method': 'channels.create'
                },
                {
                    'method': 'channels.invite'
                },
                {
                    'method': 'chat.postMessage'  # initiate discussion
                },
                {
                    'method': 'im.open'
                },
                {
                    'method': 'chat.postMessage'  # DM user discussion info
                },
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )

    def test_post_with_nonexisting_user(self, portal_client, slack_client_class, slack_agent_repository, mocker):
        mocker.spy(portal_client, 'mutate')
        mocker.spy(slack_client_class, 'api_call')
        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_interactive_component_request.team.id)

        portal_client.set_next_response(None)  # To raise error on attempt w/out user
        self._queue_portal_user_and_topic_creation(portal_client=portal_client)
        self._queue_portal_discussion_creation(portal_client=portal_client)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(self.default_payload)}))

        def wait_condition():
            return portal_client.mutate.call_count == 3 and slack_client_class.api_call.call_count >= 5
        outcome = wait_until(condition=wait_condition)
        assert outcome, 'Expected portal_client to have 3 calls, and slack_client to have 6+'

        assert HTTPStatus.OK == response.status_code
        assert 'createTopicFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert 'createUserAndTopicFromSlack' in portal_client.mutate.call_args_list[1][1]['operation_definition']
        assert 'createDiscussionFromSlack' in portal_client.mutate.call_args_list[2][1]['operation_definition']
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {
                    'method': 'users.info',
                    'user': self.fake_interactive_component_request.user.id
                },
                {
                    'method': 'channels.create'
                },
                {
                    'method': 'channels.invite'
                },
                {
                    'method': 'chat.postMessage'  # initiate discussion
                },
                {
                    'method': 'im.open'
                },
                {
                    'method': 'chat.postMessage'  # DM user discussion info
                },
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )

    def _queue_portal_topic_creation(self, portal_client, topic_id):
        portal_client.set_next_response({
            'data': {
                'createTopicFromSlack': {
                    'topic': {
                        'id': topic_id,
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

    def _queue_portal_discussion_creation(self, portal_client):
        portal_client.set_next_response({
            'data': {
                'createDiscussionFromSlack': {
                    'discussion': {
                        'id': str(PrimitiveFaker('random_int')),
                        'name': str(PrimitiveFaker('word'))
                    },
                }
            }
        })

    def _queue_portal_user_and_topic_creation(self, portal_client):
        portal_client.set_next_response({
            'data': {
                'createUserAndTopicFromSlack': {
                    'topic': {
                        'id': str(PrimitiveFaker('random_int')),
                        'title': self.fake_interactive_component_request.submission.title,
                        'description': self.fake_interactive_component_request.submission.description,
                        'tags': [
                            {'name': self.fake_tags[0].lower()},
                            {'name': self.fake_tags[1].lower()}
                        ],
                    },
                    # TODO missing user
                }
            }
        })
