from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, Date, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UserRole(str, enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    bio = Column(Text)
    avatar_url = Column(String(500))
    github_username = Column(String(100))
    twitter_username = Column(String(100))
    discord_id = Column(String(100))
    website = Column(String(255))
    country = Column(String(100))
    
    rating = Column(Integer, nullable=False, default=1000)
    max_rating = Column(Integer, nullable=False, default=1000)
    rating_volatility = Column(Float, nullable=False, default=250.0)
    
    total_solved = Column(Integer, nullable=False, default=0)
    total_points = Column(Integer, nullable=False, default=0)
    total_competitions = Column(Integer, nullable=False, default=0)
    competition_wins = Column(Integer, nullable=False, default=0)
    consecutive_days = Column(Integer, nullable=False, default=0)
    last_active_date = Column(Date)
    
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.USER)
    is_verified = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    ban_reason = Column(Text)
    
    last_login = Column(DateTime(timezone=True))
    deleted_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    submissions = relationship("Submission", back_populates="user", lazy="dynamic")
    rating_history = relationship("RatingHistory", back_populates="user", lazy="dynamic")
    achievements = relationship("UserAchievement", back_populates="user", lazy="dynamic")
    writeups = relationship("Writeup", back_populates="user", lazy="dynamic")
    team_memberships = relationship("TeamMember", back_populates="user", lazy="dynamic")
    managed_teams = relationship("Team", back_populates="captain", foreign_keys="Team.captain_id")
