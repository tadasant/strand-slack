from src.clients.PortalClient import PortalClient
from src.common.logging import get_logger


class PortalClientWrapper:
    def __init__(self, log_file):
        self.portal_client = PortalClient()
        self.logger = get_logger('PortalClientWrapper', log_file)
