import json
from copy import deepcopy
from typing import List

from src.models.Model import Model
from src.models.slack.elements.SlackElement import SlackElement


class SlackDialog(Model):
    def __init__(self, title, submit_label, callback_id, elements):
        self.title = title
        self.submit_label = submit_label
        self.callback_id = callback_id
        self.elements: List[SlackElement] = elements

    def to_json(self):
        result = deepcopy(vars(self))
        result['elements'] = [json.loads(x.to_json()) for x in self.elements]
        return json.dumps(result)
