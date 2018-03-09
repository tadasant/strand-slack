from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from src.utilities.database import Base


class Agent(Base):
    __tablename__ = 'agent'

    slack_team_id = Column(String, primary_key=True)
    strand_team_id = Column(BigInteger)
    status = Column(String)

    # 1 <--> 0..1
    bot = relationship('Bot', uselist=False, back_populates='agent')

# TODO relationships to bot, user, installation
