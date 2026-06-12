from pydantic import BaseModel
from typing import Optional, List, Any

class PaginatedResponse(BaseModel):
    items: List[Any]; total: int; page: int; pages: int; per_page: int

class MessageResponse(BaseModel):
    message: str; success: bool = True

class ErrorResponse(BaseModel):
    error: str; detail: Optional[str] = None; success: bool = False
