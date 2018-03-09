from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

from src.utilities.database import Base


class User(Base):
    __tablename__ = 'user'

    strand_user_id = Column(BigInteger)
    slack_user_id = Column(String, primary_key=True)

    # 0..* <--> 1
    agent_slack_team_id = Column(String, ForeignKey('agent.slack_team_id'), primary_key=True)
    agent = relationship('Agent', back_populates='users')

    # 1 <--> 0..1
    installation = relationship('Installation', back_populates='installer')
