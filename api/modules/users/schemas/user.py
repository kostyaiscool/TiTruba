from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    username: Optional[str] = None
    # first_name: str
    # last_name: Optional[str] = None
    language_code: Optional[str] = None

class AnonUser(BaseModel):
    language: Optional[str] = None

