from sqlalchemy import Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Agent(Base):
    __tablename__ = 'user'

    slack_team_id = Column(String, primary_key=True)
    strand_team_id = Column(BigInteger)
    status = Column(String)

# TODO relationships to bot, user, installation
