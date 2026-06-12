from sqlalchemy import Column, String, Integer, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime
import uuid, enum

class TeamStatus(str, enum.Enum): ACTIVE = 'active'; INACTIVE = 'inactive'; BANNED = 'banned'

class Team(Base):
    __tablename__ = 'teams'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    avatar_url = Column(String(500))
    captain_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    team_code = Column(String(20), unique=True, nullable=False)
    status = Column(SQLEnum(TeamStatus), default=TeamStatus.ACTIVE)
    total_members = Column(Integer, default=1)
    team_rating = Column(Integer, default=1000)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    captain = relationship('User', back_populates='managed_teams', foreign_keys=[captain_id])
    members = relationship('TeamMember', back_populates='team', lazy='dynamic')
