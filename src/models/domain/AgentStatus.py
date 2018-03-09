from enum import Enum


class AgentStatus(Enum):
    INITIATED = 'INITIATED'
    AUTHENTICATED = 'AUTHENTICATED'
    ACTIVE = 'ACTIVE'
    PAUSED = 'PAUSED'
    INACTIVE = 'INACTIVE'
