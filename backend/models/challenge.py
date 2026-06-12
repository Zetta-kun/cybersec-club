from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime
import uuid
import enum

class ChallengeCategory(str, enum.Enum):
    WEB_EXPLOITATION = "web_exploitation"
    CRYPTOGRAPHY = "cryptography"
    FORENSICS = "forensics"
    REVERSE_ENGINEERING = "reverse_engineering"
    BINARY_EXPLOITATION = "binary_exploitation"
    OSINT = "osint"
    MISC = "misc"
    MOBILE = "mobile"
    CLOUD = "cloud"
    BLOCKCHAIN = "blockchain"

class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    INSANE = "insane"

class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False, index=True)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(SQLEnum(ChallengeCategory), nullable=False, index=True)
    difficulty = Column(SQLEnum(DifficultyLevel), nullable=False, index=True)
    
    base_points = Column(Integer, nullable=False, default=100)
    min_points = Column(Integer, default=50)
    max_points = Column(Integer, default=500)
    decay_rate = Column(Float, default=0.95)
    current_points = Column(Integer, default=100)
    
    flag_hash = Column(String(255), nullable=False)
    flag_format = Column(String(50), default="CTF{...}")
    
    hints = Column(JSONB, default=[])
    files = Column(JSONB, default=[])
    tags = Column(ARRAY(String), default=[])
    prerequisites = Column(ARRAY(UUID), default=[])
    
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    total_attempts = Column(Integer, default=0)
    total_solves = Column(Integer, default=0)
    total_likes = Column(Integer, default=0)
    first_blood_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    first_blood_at = Column(DateTime(timezone=True))
    
    is_dynamic_scoring = Column(Boolean, default=True)
    is_hidden = Column(Boolean, default=False)
    is_draft = Column(Boolean, default=False)
    allow_writeups = Column(Boolean, default=True)
    
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    submissions = relationship("Submission", back_populates="challenge", lazy="dynamic")
    writeups = relationship("Writeup", back_populates="challenge", lazy="dynamic")
    author = relationship("User", foreign_keys=[author_id])
    first_blood_user = relationship("User", foreign_keys=[first_blood_user_id])
