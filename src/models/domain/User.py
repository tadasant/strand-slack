from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

from src.utilities.database import Base


class User(Base):
    __tablename__ = 'user'

    slack_user_id = Column(String(16), primary_key=True)
    strand_user_id = Column(BigInteger, nullable=True)

    # 0..* <--> 1
    agent_slack_team_id = Column(String(16), ForeignKey('agent.slack_team_id'), primary_key=True)
    agent = relationship('Agent', back_populates='users')

    # 1 <--> 0..1
    installation = relationship('Installation', back_populates='installer', cascade='all, delete-orphan')

    @staticmethod
    def is_installer(session, slack_user_id, slack_team_id):
        user = session.query(User).filter(
            User.slack_user_id == slack_user_id,
            User.agent_slack_team_id == slack_team_id
        ).one_or_none()
        return bool(user.installation if user else False)
