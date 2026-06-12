from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime
import uuid

class RatingHistory(Base):
    __tablename__ = 'rating_history'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    rating_before = Column(Integer, nullable=False)
    rating_after = Column(Integer, nullable=False)
    rating_change = Column(Integer, nullable=False)
    contest_id = Column(UUID(as_uuid=True), nullable=True)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey('challenges.id'), nullable=True)
    reason = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    user = relationship('User', back_populates='rating_history')
