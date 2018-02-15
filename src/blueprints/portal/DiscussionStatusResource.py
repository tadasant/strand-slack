from http import HTTPStatus
from threading import Thread

from flask import request, current_app

from src.blueprints.portal.PortalResource import PortalResource
from src.domain.models.portal.Discussion import DiscussionStatus
from src.service.type.DiscussionStatusChangeService import DiscussionStatusChangeService


class StaleDiscussionStatusResource(PortalResource):

    @PortalResource.authenticate
    def post(self):
        """Used for marking a discussion status as stale"""
        args = request.get_json()
        slack_channel_id = args['slack_channel_id']
        slack_team_id = args['slack_team_id']
        service = DiscussionStatusChangeService(slack_client_wrapper=current_app.slack_client_wrapper,
                                                portal_client_wrapper=current_app.portal_client_wrapper,
                                                slack_team_id=slack_team_id,
                                                slack_channel_id=slack_channel_id,
                                                discussion_status=DiscussionStatus.STALE)
        Thread(target=service.execute, daemon=True).start()

        return '', HTTPStatus.NO_CONTENT


class ClosedDiscussionStatusResource(PortalResource):

    @PortalResource.authenticate
    def post(self):
        """Used for marking a discussion status as closed"""
        args = request.get_json()
        slack_channel_id = args['slack_channel_id']
        slack_team_id = args['slack_team_id']
        service = DiscussionStatusChangeService(slack_client_wrapper=current_app.slack_client_wrapper,
                                                portal_client_wrapper=current_app.portal_client_wrapper,
                                                slack_team_id=slack_team_id,
                                                slack_channel_id=slack_channel_id,
                                                discussion_status=DiscussionStatus.CLOSED)
        Thread(target=service.execute, daemon=True).start()

        return '', HTTPStatus.NO_CONTENT