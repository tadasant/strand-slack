from flask import request

from src.blueprints.slack.SlackResource import SlackResource


class EventResource(SlackResource):
    def post(self):
        """Receiving an event from Slack"""
        self.logger.info(f'Processing Event request: {request}')
        # type == 'url_verification'
        # TODO handle channel messages as well -- do parsing of "discussions-X" after a channels.info query for now
        # later we'll replace w/ querying our own DB to check
        return request.json['challenge'], 200
