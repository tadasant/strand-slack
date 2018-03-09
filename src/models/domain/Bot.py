from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from src.utilities.database import Base


class Bot(Base):
    __tablename__ = 'bot'

    access_token = Column(String(128), nullable=False)
    user_id = Column(String(16), nullable=False)

    # 0..1 <--> 1
    agent_slack_team_id = Column(String(16), ForeignKey('agent.slack_team_id'), primary_key=True)
    agent = relationship('Agent', back_populates='bot')
