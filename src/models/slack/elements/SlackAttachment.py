import json
from copy import deepcopy
from typing import List

from src.models.Model import Model
from src.models.slack.elements.SlackAction import SlackAction


class SlackAttachment(Model):
    def __init__(self, fallback=None, color=None, author_name=None, fields=None, footer=None, footer_icon=None,
                 ts=None, callback_id=None, attachment_type=None, actions=None, type=None, value=None):
        self.fallback = fallback
        self.color = color
        self.author_name = author_name
        self.fields = fields
        self.footer = footer
        self.footer_icon = footer_icon
        self.ts = ts
        self.callback_id = callback_id
        self.attachment_type = attachment_type
        self.type = type
        self.value = value
        self.actions: List[SlackAction] = actions

    def to_json(self):
        result = deepcopy(vars(self))
        result['actions'] = [json.loads(x.to_json()) for x in self.actions]
        return json.dumps(result)
