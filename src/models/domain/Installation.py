from sqlalchemy import Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Installation(Base):
    __tablename__ = 'user'

    installer_slack_user_id = Column(String, primary_key=True)
    access_token = Column(BigInteger)
    scope = Column(String)

# TODO relationship to agent (nullable many to one)
