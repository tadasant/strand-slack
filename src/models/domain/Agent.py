from enum import Enum as PythonEnum

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SAEnum

from src.utilities.database import Base


class AgentStatus(PythonEnum):
    INITIATED = 'INITIATED'
    AUTHENTICATED = 'AUTHENTICATED'
    ACTIVE = 'ACTIVE'
    PAUSED = 'PAUSED'
    INACTIVE = 'INACTIVE'


class Agent(Base):
    __tablename__ = 'agent'

    slack_team_id = Column(String(16), primary_key=True)
    strand_team_id = Column(BigInteger)
    status = Column(SAEnum(AgentStatus), nullable=False)

    # 1 <--> 0..1
    bot = relationship('Bot', uselist=False, back_populates='agent', cascade='all, delete-orphan')
    # 1 <--> 0..*
    users = relationship('User', back_populates='agent', cascade='all, delete-orphan')
