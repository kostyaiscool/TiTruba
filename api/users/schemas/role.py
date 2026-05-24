from pydantic import BaseModel
from typing import Optional


class Role(BaseModel):
    id: int
    name: Optional[str] = None

class Permission(BaseModel):
    id: int
    name: Optional[str] = None