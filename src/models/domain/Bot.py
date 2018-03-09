from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Bot(Base):
    __tablename__ = 'bot'

    bot_access_token = Column(String)
    bot_user_id = Column(String)

# TODO relationship to agent (nullable one to one, PK)
