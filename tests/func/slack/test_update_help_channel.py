import pytest

from src.config import config
from tests.factories.slackfactories import InteractiveMenuResponseFactory, ActionFactory, OptionFactory


@pytest.mark.usefixtures('client_class')  # pytest-flask's client_class adds self.client
class TestUpdateHelpChannel:
    # For assertions
    fake_interactive_menu_response = InteractiveMenuResponseFactory.create()

    # For setup
    target_endpoint = 'slack.interactivecomponentresource'
    default_payload = {
        'type': fake_interactive_menu_response.type,
        'actions': [
            {
                'name': fake_interactive_menu_response.actions[0].name,
                'type': 'select',
                'selected_options': [
                    {
                        'value': 'C1DFRD2GZ'
                    }
                ]
            }
        ],
        'callback_id': fake_interactive_menu_response.callback_id,
        'team': {
            'id': fake_interactive_menu_response.team.id,
            'domain': 'solutionloft'
        },
        'channel': {
            'id': 'D8YS0A9D1',
            'name': 'directmessage'
        },
        'user': {
            'id': 'U7JH1V2PP',
            'name': 'tadas'
        },
        'action_ts': '1517014983.191305',
        'message_ts': '1517014969.000145',
        'attachment_id': '1',
        'token': config['SLACK_VERIFICATION_TOKEN'],
        'is_app_unfurl': False,
        'original_message': {
            'text': fake_interactive_menu_response.original_message.text,
            'username': 'CodeClippy',
            'bot_id': 'B8Y9T3Z3J',
            'attachments': [
                {
                    'callback_id': 'onboarding_dm',
                    'fallback': 'Upgrade your Slack client to use messages like these.',
                    'id': 1,
                    'color': '3AA3E3',
                    'actions': [
                        {
                            'id': '1',
                            'name': 'help_channel_list',
                            'text': 'What channel should I use for showing help requests?',
                            'type': 'select',
                            'data_source': 'channels'
                        }
                    ]
                }
            ],
            'type': 'message',
            'subtype': 'bot_message',
            'ts': '1517014969.000145'
        },
        'response_url': fake_interactive_menu_response.response_url,
        'trigger_id': '304946943568.10642948979.fde99265c25c102dc631e6cd49ac4535'
    }

    def test_post_valid_unauthenticated_slack(self, slack_agent_repository, test_slack_client_class, mocker):
        pass
        # with pytest.raises(RepositoryException):
        #     slack_agent_repository.get_slack_bot_access_token(slack_team_id=self.fake_slack_team_id)
        #
        # mocker.spy(test_slack_client_class, 'api_call')
        # mocker.spy(test_slack_client_class, '__init__')
        # target_url = url_for(endpoint=self.target_endpoint)
        #
        # response = self.client.post(path=target_url, headers=self.default_headers,
        #                             data=json.dumps(self.default_payload))
        #
        # # Some data is returned, bot token is stored in repo, and onboarding DM was called w/ correct token
        # data = json.loads(response.data)
        # assert data['slack_application_installation']['installer']['id'] == self.fake_installer_id
        # assert slack_agent_repository.get_slack_bot_access_token(
        #     slack_team_id=self.fake_slack_team_id) == self.fake_slack_bot_access_token
        # assert test_slack_client_class.api_call.call_count == 2
        # assert test_slack_client_class.__init__.call_args[1]['token'] == self.fake_slack_bot_access_token

    def test_post_valid_authenticated_slack(self, slack_agent_repository):
        pass
