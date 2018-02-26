import json

from flask import url_for

from src.config import config
from src.domain.models.portal.SlackAgent import SlackAgent
from src.domain.models.portal.SlackAgentStatus import SlackAgentStatus
from src.domain.models.portal.SlackApplicationInstallation import SlackApplicationInstallation
from src.domain.models.portal.SlackTeam import SlackTeam
from src.domain.models.portal.SlackUser import SlackUser
from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.factories.portalfactories import SlackAgentFactory


def test_doesnt_send_onboarding_message_on_topic_channel_update(slack_client_class, slack_agent_repository, client,
                                                                mocker):
    # TODO [SLA-106] use fixtures instead of this WET setup code
    # GIVEN: An existing slackagent in the repository
    fake_slack_agent = SlackAgentFactory.build()
    fake_slack_team_id = fake_slack_agent.slack_team.id
    fake_slack_access_token = fake_slack_agent.slack_application_installation.access_token
    fake_slack_bot_access_token = fake_slack_agent.slack_application_installation.bot_access_token
    fake_installer_id = fake_slack_agent.slack_application_installation.installer.id
    slack_agent_repository.add_slack_agent(slack_agent=SlackAgent(
        status=SlackAgentStatus.ACTIVE,
        slack_team=SlackTeam(id=fake_slack_team_id),
        topic_channel_id=fake_slack_agent.topic_channel_id,
        slack_application_installation=SlackApplicationInstallation(access_token='doesnt matter',
                                                                    installer=SlackUser(id=fake_installer_id),
                                                                    bot_access_token='doesnt matter',
                                                                    bot_user_id='doesnt matter'))
    )

    # WHEN: A request comes from API with an updated topic channel ID
    target_url = url_for(endpoint='portal.slackagentresource')
    fake_new_topic_channel_id = str(PrimitiveFaker('bban'))
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {config["PORTAL_VERIFICATION_TOKEN"]}'
    }
    payload = {
        'status': fake_slack_agent.status,
        'topic_channel_id': fake_new_topic_channel_id,
        'slack_team': {
            'id': fake_slack_team_id
        },
        'slack_application_installation': {
            'access_token': fake_slack_access_token,
            'installer': {
                'id': fake_installer_id,
            },
            'bot_access_token': fake_slack_bot_access_token,
            'bot_user_id': fake_slack_agent.slack_application_installation.bot_user_id
        },
    }
    mocker.spy(slack_client_class, 'api_call')
    client.put(path=target_url, headers=headers, data=json.dumps(payload))

    # ASSERT: We replaced the SlackAgent in the repository and did not re-send the onboarding message
    assert slack_agent_repository.get_slack_agent(
        slack_team_id=fake_slack_team_id
    ).topic_channel_id == fake_new_topic_channel_id
    assert slack_client_class.api_call.call_count == 0
