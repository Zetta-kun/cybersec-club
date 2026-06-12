from pydantic import BaseModel, Field, validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class ChallengeCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20)
    category: str; difficulty: str
    base_points: int = Field(100, ge=50, le=1000)
    flag: str = Field(..., min_length=5)
    flag_format: str = "CTF{...}"
    hints: List[dict] = []; files: List[dict] = []; tags: List[str] = []
    is_draft: bool = False
    @validator('category')
    def validate_category(cls, v):
        valid = ['web_exploitation', 'cryptography', 'forensics', 'reverse_engineering', 'binary_exploitation', 'osint', 'misc', 'mobile', 'cloud', 'blockchain']
        if v not in valid: raise ValueError(f'Yanlış kateqoriya')
        return v
    @validator('difficulty')
    def validate_difficulty(cls, v):
        if v not in ['easy', 'medium', 'hard', 'expert', 'insane']: raise ValueError('Yanlış çətinlik')
        return v

class FlagSubmission(BaseModel):
    challenge_id: UUID
    flag: str = Field(..., min_length=3)

class FlagResponse(BaseModel):
    status: str; message: str; points_earned: int = 0
    is_first_blood: bool = False; attempts: int = 1
