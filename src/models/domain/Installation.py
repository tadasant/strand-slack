from sqlalchemy import Column, BigInteger, String

from src.utilities.database import Base


class Installation(Base):
    __tablename__ = 'installation'

    installer_slack_user_id = Column(String, primary_key=True)
    access_token = Column(BigInteger)
    scope = Column(String)

# TODO relationship to agent (nullable many to one)
