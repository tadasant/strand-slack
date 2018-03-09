from sqlalchemy import Column, BigInteger, String, Enum
from sqlalchemy.orm import relationship

from src.models.domain.AgentStatus import AgentStatus
from src.utilities.database import Base


class Agent(Base):
    __tablename__ = 'agent'

    slack_team_id = Column(String, primary_key=True, length=16)
    strand_team_id = Column(BigInteger)
    status = Column(Enum(AgentStatus), nullable=False)

    # 1 <--> 0..1
    bot = relationship('Bot', uselist=False, back_populates='agent')
    # 1 <--> 0..*
    users = relationship('User', back_populates='agent')

# TODO relationships to bot, user, installation
