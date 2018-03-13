import pytest

from tests.func.slack.TestHelpDmFixtures import TestHelpDmFixtures


@pytest.mark.usefixtures('app')
class TestHelpDm(TestHelpDmFixtures):
    """Test the flow for a user installing the Slack application (/install)"""

    target_endpoint = 'configure.installresource'
    default_headers = {'Content-Type': 'application/json'}

    def test_install_new_agent_new_user(self, slack_oauth_access, client, slack_client_class, strand_api_client,
                                        db_session, mocker, baseline_thread_count):
        """
            GIVEN:
            OUTPUT:
        """
        pass
