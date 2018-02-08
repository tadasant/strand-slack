import json
from copy import deepcopy
from http import HTTPStatus
from urllib.parse import urlencode

from flask import url_for

from src.command.messages.post_topic_dialog import POST_TOPIC_DIALOG
from src.config import config
from src.domain.models.portal.SlackAgent import SlackAgent
from src.domain.models.portal.SlackAgentStatus import SlackAgentStatus
from src.domain.models.portal.SlackApplicationInstallation import SlackApplicationInstallation
from src.domain.models.portal.SlackTeam import SlackTeam
from src.domain.models.portal.SlackUser import SlackUser
from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.factories.slackfactories import SubmissionFactory, InteractiveComponentRequestFactory
from tests.func.TestFunction import TestFunction
from tests.testresources.TestSlackClient import SlackRepository
from tests.utils import wait_until


class TestSlackFunction(TestFunction):
    default_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def assert_values_in_call_args_list(self, params_to_expecteds, call_args_list, expect_succeed=True):
        """
        Asserts that a subset of each item in params_to_expecteds exists in the call args list.

        If expect_succeed is False, will return the inverse. Useful when checking to make sure calls DIDN'T happen.

        :param params_to_expecteds: e.g. [{'paramname': 'expectedval', 'param2name': 'expected2val}]
        """
        params_to_actuals = [x[1] for x in call_args_list]
        original_params_to_expecteds = deepcopy(params_to_expecteds)
        for i, expected in enumerate(original_params_to_expecteds):
            for j, actual in enumerate(params_to_actuals):
                if all(item in actual.items() for item in expected.items()):
                    params_to_expecteds[i] = None
                    params_to_actuals[j] = {}
                    break

        condition = len([x for x in params_to_expecteds if x is not None]) == 0
        assert condition if expect_succeed else not condition, f'{params_to_expecteds} vs. {params_to_actuals}'

    def add_slack_agent_to_repository(self, slack_agent_repository, slack_team_id, installer_user_id='doesnt matter'):
        slack_agent_repository.add_slack_agent(slack_agent=SlackAgent(
            status=SlackAgentStatus.ACTIVE,
            slack_team=SlackTeam(id=slack_team_id),
            topic_channel_id=str(PrimitiveFaker('bban')),
            slack_application_installation=SlackApplicationInstallation(access_token='doesnt matter',
                                                                        installer=SlackUser(id=installer_user_id),
                                                                        bot_access_token='doesnt matter',
                                                                        bot_user_id='doesnt matter'))
        )

    def start_discussion_on_channel(self, slack_team_id, portal_client, slack_agent_repository, slack_client_class,
                                    mocker):
        self.start_discussion(slack_agent_repository=slack_agent_repository,
                              slack_team_id=slack_team_id,
                              slack_client_class=slack_client_class,
                              portal_client=portal_client,
                              mocker=mocker)
        assert 1 == len(SlackRepository['created_channels_by_id'].items())
        # return created channel id
        return next(iter(SlackRepository['created_channels_by_id'].values()))['id']

    def start_discussion(self, slack_agent_repository, slack_team_id, slack_client_class, portal_client, mocker,
                         topic_id=int(str(PrimitiveFaker('random_int')))):
        """
            Starts a discussion on slack_team_id.

            TODO This needs to be cleaned up. Create some sort of constructor for Slack payloads.
        """
        # TODO update discussion tests to use this as well
        mocker.spy(portal_client, 'mutate')
        mocker.spy(slack_client_class, 'api_call')
        discussion_dialog_post_endpoint = 'slack.interactivecomponentresource'
        target_url = url_for(endpoint=discussion_dialog_post_endpoint)
        self.simulate_topic_channel_initiation(slack_agent_repository=slack_agent_repository,
                                               slack_team_id=slack_team_id)

        self.__queue_portal_topic_creation(portal_client=portal_client, topic_id=topic_id)
        self.__queue_portal_discussion_creation(portal_client=portal_client)

        fake_tags = [str(PrimitiveFaker('word')), str(PrimitiveFaker('word'))]
        fake_interactive_component_request = InteractiveComponentRequestFactory.create(
            submission=SubmissionFactory.create(tags=', '.join(fake_tags)),
            callback_id=POST_TOPIC_DIALOG.callback_id,
            type='dialog_submission'
        )
        payload = {
            "type": fake_interactive_component_request.type,
            "callback_id": fake_interactive_component_request.callback_id,
            "submission": {
                "title": fake_interactive_component_request.submission.title,
                "description": fake_interactive_component_request.submission.description,
                "tags": fake_interactive_component_request.submission.tags
            },
            "team": {
                "id": slack_team_id,
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
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = self.client.post(path=target_url, headers=headers,
                                    data=urlencode({'payload': json.dumps(payload)}))

        def wait_condition():
            return portal_client.mutate.call_count == 2 and slack_client_class.api_call.call_count >= + 8

        assert HTTPStatus.OK == response.status_code
        wait_until(condition=wait_condition)
        mocker.stopall()

    def simulate_topic_channel_initiation(self, slack_agent_repository, slack_team_id):
        topic_channel_id = slack_agent_repository.get_topic_channel_id(slack_team_id=slack_team_id)
        if topic_channel_id not in SlackRepository['messages_posted_by_channel_id']:
            SlackRepository['messages_posted_by_channel_id'][topic_channel_id] = []
        SlackRepository['messages_posted_by_channel_id'][topic_channel_id].append(
            {'ts': str(PrimitiveFaker('random_int')), 'text': 'sometext', 'attachments': []}
        )

    def __queue_portal_topic_creation(self, portal_client, topic_id=1, topic_title='sometitle',
                                      topic_description='somedesc', tag_name1='some1tag', tag_name2='some2tag'):
        portal_client.set_next_response({
            'data': {
                'createTopicFromSlack': {
                    'topic': {
                        'id': topic_id,
                        'title': topic_title,
                        'description': topic_description,
                        'tags': [
                            {'name': tag_name1.lower()},
                            {'name': tag_name2.lower()}
                        ],
                    },
                }
            }
        })

    def __queue_portal_discussion_creation(self, portal_client):
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
