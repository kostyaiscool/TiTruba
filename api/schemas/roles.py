from typing import List

from pydantic import BaseModel, ConfigDict

from schemas.permissions import PermissionRead


class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    permissions: List[PermissionRead] = []

class RoleCreate(BaseModel):
    name: str
