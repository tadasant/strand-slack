from typing import NamedTuple

import pytest


class TestHelpDmFixtures:
    @pytest.fixture(scope='function')
    def slack_oauth_access(self, slack_oauth_access_response_factory) -> NamedTuple:
        """
            Yield
        """
        pass
