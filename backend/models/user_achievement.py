from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime
import uuid

class UserAchievement(Base):
    __tablename__ = 'user_achievements'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    achievement_id = Column(UUID(as_uuid=True), ForeignKey('achievements.id'), nullable=False)
    progress = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    user = relationship('User', back_populates='achievements')
    achievement = relationship('Achievement', back_populates='user_achievements')
