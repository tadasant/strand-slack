from copy import deepcopy

from tests.func.slack.TestInteractiveComponent import TestInteractiveComponent


class TestButton(TestInteractiveComponent):
    default_payload = deepcopy(TestInteractiveComponent.default_payload)
    del default_payload['type']  # not sent with buttons
