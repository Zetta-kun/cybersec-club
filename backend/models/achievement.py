from sqlalchemy import Column, String, Integer, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime
import uuid, enum
from sqlalchemy.dialects.postgresql import UUID

class AchievementType(str, enum.Enum):
    FIRST_BLOOD = 'first_blood'; STREAK = 'streak'; CHALLENGE_COUNT = 'challenge_count'
    COMPETITION_WIN = 'competition_win'; CATEGORY_MASTER = 'category_master'

class Achievement(Base):
    __tablename__ = 'achievements'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    type = Column(SQLEnum(AchievementType), nullable=False)
    icon_url = Column(String(500))
    required_value = Column(Integer, default=1)
    points_reward = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    user_achievements = relationship('UserAchievement', back_populates='achievement', lazy='dynamic')
