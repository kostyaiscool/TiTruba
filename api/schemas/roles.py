from typing import TYPE_CHECKING, List

from pydantic import BaseModel

if TYPE_CHECKING:
    from schemas.permissions import PermissionRead

class RoleRead(BaseModel):
    id: int
    name: str
    permission: List[PermissionRead]

class RoleCreate(BaseModel):
    name: str