import json
from http import HTTPStatus

import pytest
from flask import url_for

from src.models.domain.Agent import Agent
from src.models.domain.Bot import Bot
from src.models.domain.Installation import Installation
from tests.factories.slackfactories import SlackEventFactory, SlackTokensFactory
from tests.func.slack.TestSlackFixtures import TestSlackFixtures
from tests.utils.asserting import wait_for_extra_threads_to_die


@pytest.mark.usefixtures('app')
class TestRemovals(TestSlackFixtures):
    """Test the flow for a user copy/pasting a strand into DM"""

    target_endpoint = 'slack.eventresource'
    default_headers = {'Content-Type': 'application/json'}

    def test_remove_application(self, installed_agent: Agent, slack_event_request_factory, slack_client_class,
                                baseline_thread_count, client, mocker, db_session):
        """Remove the agent when receiving a slack event regarding application removal"""
        assert 1 == db_session.query(Agent).filter_by(slack_team_id=installed_agent.slack_team_id).count()
        target_url = url_for(endpoint=self.target_endpoint)
        fake_slack_event_request = slack_event_request_factory(
            type='event_callback',
            challenge=None,
            team_id=installed_agent.slack_team_id,
            event=SlackEventFactory.create(
                type='app_uninstalled'
            )
        )
        payload = json.loads(fake_slack_event_request.to_json())
        mocker.spy(slack_client_class, 'api_call')

        response = client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))
        assert wait_for_extra_threads_to_die(baseline_count=baseline_thread_count), 'Extra threads timed out'
        assert HTTPStatus.OK == response.status_code

        assert 0 == db_session.query(Agent).filter_by(slack_team_id=installed_agent.slack_team_id).count()

    def test_remove_bots_and_installations(self, installed_agent: Agent, slack_event_request_factory,
                                           slack_client_class, baseline_thread_count, client, mocker, db_session):
        """Remove the bot and installer when receiving a slack event regarding tokens revoked"""
        assert 1 == db_session.query(Bot).filter_by(agent_slack_team_id=installed_agent.slack_team_id).count()
        assert 1 == db_session.query(Installation).filter_by(
            installer_agent_slack_team_id=installed_agent.slack_team_id).count()
        assert 1 == db_session.query(Agent).filter_by(slack_team_id=installed_agent.slack_team_id).count()
        target_url = url_for(endpoint=self.target_endpoint)
        oauth_token = installed_agent.users[0].installation[0].access_token
        bot_token = installed_agent.bot.access_token
        fake_slack_event_request = slack_event_request_factory(
            type='event_callback',
            challenge=None,
            team_id=installed_agent.slack_team_id,
            event=SlackEventFactory.create(
                type='tokens_revoked',
                tokens=SlackTokensFactory.create(
                    oauth=[oauth_token],
                    bot=[bot_token]
                ),
            ),
        )
        payload = json.loads(fake_slack_event_request.to_json())
        mocker.spy(slack_client_class, 'api_call')

        response = client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))
        assert wait_for_extra_threads_to_die(baseline_count=baseline_thread_count), 'Extra threads timed out'
        assert HTTPStatus.OK == response.status_code

        assert 0 == db_session.query(Bot).filter_by(agent_slack_team_id=installed_agent.slack_team_id).count()
        assert 0 == db_session.query(Installation).filter_by(
            installer_agent_slack_team_id=installed_agent.slack_team_id).count()
        assert 1 == db_session.query(Agent).filter_by(slack_team_id=installed_agent.slack_team_id).count()
