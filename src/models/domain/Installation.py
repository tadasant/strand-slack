from sqlalchemy import Column, String, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from src.models.domain.User import User
from src.utilities.database import Base


class Installation(Base):
    __tablename__ = 'installation'

    access_token = Column(String(128), nullable=False)
    scope = Column(String(256), nullable=False)

    # 0..1 <--> 1
    installer_slack_user_id = Column(String(16), primary_key=True)
    installer_agent_slack_team_id = Column(String(16), primary_key=True)
    installer = relationship('User', back_populates='installation')

    # Composite foreign key
    __table_args__ = (ForeignKeyConstraint([installer_slack_user_id, installer_agent_slack_team_id],
                                           [User.slack_user_id, User.agent_slack_team_id]),)
