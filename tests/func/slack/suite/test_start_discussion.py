import json
from copy import deepcopy
from http import HTTPStatus
from urllib.parse import urlencode

from flask import url_for

from src.command.model.message.post_topic_dialog import POST_TOPIC_DIALOG
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
            "id": fake_interactive_component_request.channel.id,
            "name": fake_interactive_component_request.channel.name
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
        payload = deepcopy(self.default_payload)
        payload['token'] = 'unverified-token'
        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(payload)}))
        assert response.json['error'] == 'Invalid slack verification token'

    def test_post_valid_authenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(self.default_payload)}))
        assert HTTPStatus.OK == response.status_code

    def validate_post(self, portal_client, slack_agent_repository, slack_client_class, mocker, payload,
                      params_to_expect, param_to_expect, expect_to_succeed):
        mocker.spy(portal_client, 'mutate')
        mocker.spy(slack_client_class, 'api_call')
        target_url = url_for(endpoint=self.target_endpoint)
        fake_topic_id = int(str(PrimitiveFaker('random_int')))
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_interactive_component_request.team.id)
        self._queue_portal_topic_creation(portal_client=portal_client, topic_id=fake_topic_id)
        self._queue_portal_discussion_creation(portal_client=portal_client)
        self.simulate_topic_channel_initiation(slack_agent_repository=slack_agent_repository,
                                               slack_team_id=self.fake_interactive_component_request.team.id)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(payload)}))

        def wait_condition():
            return portal_client.mutate.call_count == 2 and slack_client_class.api_call.call_count >= 8

        outcome = wait_until(condition=wait_condition)
        assert outcome, 'Expected portal_client to have 2 calls, and slack_client to have 8+'

        assert HTTPStatus.OK == response.status_code
        assert 'createTopicFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert 'createDiscussionFromSlack' in portal_client.mutate.call_args_list[1][1]['operation_definition']
        assert str(fake_topic_id) in portal_client.mutate.call_args_list[1][1]['operation_definition']
        print(slack_client_class.api_call.call_args_list)
        self.assert_values_in_call_args_list(
            params_to_expecteds=params_to_expect,
            call_args_list=slack_client_class.api_call.call_args_list
        )
        self.assert_value_in_call_args_list(param_to_expect=param_to_expect,
                                            call_args_list=slack_client_class.api_call.call_args_list,
                                            expect_to_succeed=expect_to_succeed)

    def test_post_with_existing_user_and_share_to_channel(self, portal_client, slack_agent_repository,
                                                          slack_client_class, mocker):
        payload = deepcopy(self.default_payload)
        payload['channel']['id'] = 'C0G9QPY56'
        payload['submission']['share_with_current_channel'] = 'True'
        params_to_expect = [
            {'method': 'channels.create'},  # create discussion channel
            {'method': 'channels.invite'},  # invite bot
            {'method': 'channels.invite'},  # invite user
            {'method': 'chat.postMessage'},  # initiate discussion
            {'method': 'im.open'},  # Open user DM
            {'method': 'chat.postMessage'},  # DM user discussion info
            {'method': 'channels.history'},  # Grabbing last post in topic channel
            {'method': 'chat.update'},  # Updating last post with topic info
            {'method': 'chat.postMessage'},  # Re-posting last post
            {'method': 'chat.postMessage'},  # Share to channel
        ]
        param_to_expect = {'method': 'chat.postMessage', 'channel': payload['channel']['id']}
        self.validate_post(portal_client, slack_agent_repository, slack_client_class, mocker, payload,
                           params_to_expect=params_to_expect, param_to_expect=param_to_expect, expect_to_succeed=True)

    def test_post_with_existing_user_and_do_not_share_to_channel(self, portal_client, slack_agent_repository,
                                                                 slack_client_class, mocker):
        payload = deepcopy(self.default_payload)
        payload['channel']['id'] = 'C0G9QPY56'
        payload['submission']['share_with_current_channel'] = 'False'
        params_to_expect = [
            {'method': 'channels.create'},  # create discussion channel
            {'method': 'channels.invite'},  # invite bot
            {'method': 'channels.invite'},  # invite user
            {'method': 'chat.postMessage'},  # initiate discussion
            {'method': 'im.open'},  # Open user DM
            {'method': 'chat.postMessage'},  # DM user discussion info
            {'method': 'channels.history'},  # Grabbing last post in topic channel
            {'method': 'chat.update'},  # Updating last post with topic info
            {'method': 'chat.postMessage'},  # Re-posting last post
        ]
        param_to_expect = {'method': 'chat.postMessage', 'channel': payload['channel']['id']}
        self.validate_post(portal_client, slack_agent_repository, slack_client_class, mocker, payload,
                           params_to_expect=params_to_expect, param_to_expect=param_to_expect, expect_to_succeed=False)

    def test_post_with_existing_user(self, portal_client, slack_agent_repository, slack_client_class, mocker):
        mocker.spy(portal_client, 'mutate')
        mocker.spy(slack_client_class, 'api_call')
        target_url = url_for(endpoint=self.target_endpoint)
        fake_topic_id = int(str(PrimitiveFaker('random_int')))
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_interactive_component_request.team.id)
        self._queue_portal_topic_creation(portal_client=portal_client, topic_id=fake_topic_id)
        self._queue_portal_discussion_creation(portal_client=portal_client)
        self.simulate_topic_channel_initiation(slack_agent_repository=slack_agent_repository,
                                               slack_team_id=self.fake_interactive_component_request.team.id)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(self.default_payload)}))

        def wait_condition():
            return portal_client.mutate.call_count == 2 and slack_client_class.api_call.call_count >= 8

        outcome = wait_until(condition=wait_condition)
        assert outcome, 'Expected portal_client to have 2 calls, and slack_client to have 8+'

        assert HTTPStatus.OK == response.status_code
        assert 'createTopicFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert 'createDiscussionFromSlack' in portal_client.mutate.call_args_list[1][1]['operation_definition']
        assert str(fake_topic_id) in portal_client.mutate.call_args_list[1][1]['operation_definition']
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'channels.create'},
                {'method': 'channels.invite'},  # invite bot
                {'method': 'channels.invite'},  # invite user
                {'method': 'chat.postMessage'},  # initiate discussion
                {'method': 'im.open'},
                {'method': 'chat.postMessage'},  # DM user discussion info
                {'method': 'channels.history'},  # Grabbing last post in topic channel
                {'method': 'chat.update'},  # Updating last post with topic info
                {'method': 'chat.postMessage'},  # Re-posting last post
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )

    def test_post_with_installer_user(self, portal_client, slack_agent_repository, slack_client_class, mocker):
        mocker.spy(portal_client, 'mutate')
        mocker.spy(slack_client_class, 'api_call')
        target_url = url_for(endpoint=self.target_endpoint)
        fake_installer_user_id = str(PrimitiveFaker('bban'))
        payload = deepcopy(self.default_payload)
        payload['user']['id'] = fake_installer_user_id
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_interactive_component_request.team.id,
                                           installer_user_id=fake_installer_user_id)
        self._queue_portal_topic_creation(portal_client=portal_client, topic_id=str(PrimitiveFaker('random_int')))
        self._queue_portal_discussion_creation(portal_client=portal_client)
        self.simulate_topic_channel_initiation(slack_agent_repository=slack_agent_repository,
                                               slack_team_id=self.fake_interactive_component_request.team.id)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(payload)}))

        def wait_condition():
            return portal_client.mutate.call_count == 2 and slack_client_class.api_call.call_count >= 7

        outcome = wait_until(condition=wait_condition)
        assert outcome, 'Expected portal_client to have 2 calls, and slack_client to have 7+'

        assert HTTPStatus.OK == response.status_code
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'channels.invite'},  # invite bot
                {'method': 'channels.invite'},  # invite user (shouldn't happen)
            ],
            call_args_list=slack_client_class.api_call.call_args_list,
            expect_succeed=False
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
        self.simulate_topic_channel_initiation(slack_agent_repository=slack_agent_repository,
                                               slack_team_id=self.fake_interactive_component_request.team.id)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(self.default_payload)}))

        def wait_condition():
            return portal_client.mutate.call_count == 3 and slack_client_class.api_call.call_count >= 9

        outcome = wait_until(condition=wait_condition)
        assert outcome, 'Expected portal_client to have 3 calls, and slack_client to have 9+'

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
                {'method': 'channels.create'},
                {'method': 'channels.invite'},  # invite bot
                {'method': 'channels.invite'},  # invite user
                {'method': 'chat.postMessage'},  # initiate discussion
                {'method': 'im.open'},
                {'method': 'chat.postMessage'},  # DM user discussion info
                {'method': 'channels.history'},  # Grabbing last post in topic channel
                {'method': 'chat.update'},  # Updating last post with topic info
                {'method': 'chat.postMessage'},  # Re-posting last post
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
                        'id': int(str(PrimitiveFaker('random_int'))),
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
                        'id': int(str(PrimitiveFaker('random_int'))),
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
