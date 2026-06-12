from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime
import uuid

class TeamMember(Base):
    __tablename__ = 'team_members'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    role = Column(String(50), default='member')
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    team = relationship('Team', back_populates='members')
    user = relationship('User', back_populates='team_memberships')
