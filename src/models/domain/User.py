from sqlalchemy import Column, BigInteger, String
from src.utilities.database import Base


class User(Base):
    __tablename__ = 'user'

    strand_user_id = Column(BigInteger, primary_key=True)
    slack_user_id = Column(String, primary_key=True)

# TODO relationship to agent (nullable many to one, composition, PK)
