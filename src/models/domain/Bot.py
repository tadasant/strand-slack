from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from src.utilities.database import Base


class Bot(Base):
    __tablename__ = 'bot'

    access_token = Column(String, nullable=False, length=128)
    user_id = Column(String, nullable=False, length=16)

    # 0..1 <--> 1
    agent_slack_team_id = Column(String, ForeignKey('agent.slack_team_id'), primary_key=True, length=16)
    agent = relationship('Agent', back_populates='bot')
