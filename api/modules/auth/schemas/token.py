from pydantic import BaseModel
from typing import Optional


class RefreshToken(BaseModel):
    lifetime: int = int


class AccessToken(BaseModel):
    lifetime: int = int
