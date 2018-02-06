# import json
# from copy import deepcopy
# from http import HTTPStatus
# from urllib.parse import urlencode
#
# from flask import url_for
#
# from src.config import config
# from tests.common.PrimitiveFaker import PrimitiveFaker
# from tests.factories.slackfactories import SlashCommandRequestFactory
# from tests.func.slack.TestSlackFunction import TestSlackFunction
# from tests.utils import wait_until
#
#
# class TestCloseDiscussion(TestSlackFunction):
#     # For assertions
#     fake_slash_command_request = SlashCommandRequestFactory.create()
#
#     # For setup
#     target_endpoint = 'slack.slashcommandresource'
#     default_payload = {
#         'token': config["SLACK_VERIFICATION_TOKEN"],
#         'team_id': fake_slash_command_request.team_id,
#         'team_domain': 'doesnt matter',
#         'channel_id': 'doesnt matter',
#         'channel_name': 'doesnt matter',
#         'user_id': fake_slash_command_request.user_id,
#         'user_name': 'doesnt matter',
#         'command': fake_slash_command_request.command,
#         'text': fake_slash_command_request.text,
#         'response_url': fake_slash_command_request.response_url,
#         'trigger_id': fake_slash_command_request.trigger_id
#     }
#
#     def test_post_valid_unauthenticated_slack(self):
#         target_url = url_for(endpoint=self.target_endpoint)
#         payload = deepcopy(self.default_payload)
#         payload['token'] = 'unverified-token'
#         response = self.client.post(path=target_url, headers=self.default_headers,
#                                     data=urlencode({'payload': json.dumps(payload)}))
#         assert response.json['error'] == 'Invalid slack verification token'
#
#     def test_post_with_existing_user(self, portal_client, slack_agent_repository, slack_client_class, mocker):
#         mocker.spy(portal_client, 'mutate')
#         mocker.spy(slack_client_class, 'api_call')
#         target_url = url_for(endpoint=self.target_endpoint)
#         fake_topic_id = int(str(PrimitiveFaker('random_int')))
#         self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
#                                            slack_team_id=self.fake_interactive_component_request.team.id)
#         self._queue_portal_topic_creation(portal_client=portal_client, topic_id=fake_topic_id)
#         self._queue_portal_discussion_creation(portal_client=portal_client)
#
#         response = self.client.post(path=target_url, headers=self.default_headers,
#                                     data=urlencode({'payload': json.dumps(self.default_payload)}))
#
#         def wait_condition():
#             return portal_client.mutate.call_count == 2 and slack_client_class.api_call.call_count >= 8
#
#         outcome = wait_until(condition=wait_condition)
#         assert outcome, 'Expected portal_client to have 2 calls, and slack_client to have 8+'
#
#         assert HTTPStatus.OK == response.status_code
#         assert 'createTopicFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
#         assert 'createDiscussionFromSlack' in portal_client.mutate.call_args_list[1][1]['operation_definition']
#         assert str(fake_topic_id) in portal_client.mutate.call_args_list[1][1]['operation_definition']
#         self.assert_values_in_call_args_list(
#             params_to_expecteds=[
#                 {'method': 'channels.create'},
#                 {'method': 'channels.invite'},  # invite bot
#                 {'method': 'channels.invite'},  # invite user
#                 {'method': 'chat.postMessage'},  # initiate discussion
#                 {'method': 'im.open'},
#                 {'method': 'chat.postMessage'},  # DM user discussion info
#                 {'method': 'channels.history'},  # Grabbing last post in #discuss
#                 {'method': 'chat.update'},  # Updating last post with topic info
#                 {'method': 'chat.postMessage'},  # Re-posting last post
#             ],
#             call_args_list=slack_client_class.api_call.call_args_list
#         )
#
#     def _queue_portal_close_discussion(self, portal_client, discussion_id):
#         portal_client.set_next_response({
#             'data': {
#                 'closeDiscussionFromSlack': {
#                     'discussion': {
#                         'id': discussion_id,
#                     },
#                 }
#             }
#         })
