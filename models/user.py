from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    username: str = Field(..., min_length=3)
    full_name: Optional[str] = None
    hashed_password: str  # nunca expor em respostas públicas
    disabled: bool = False

class UserPublic(BaseModel):
    username: str
    full_name: Optional[str] = None
