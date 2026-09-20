from typing import TYPE_CHECKING, List

from pydantic import BaseModel

if TYPE_CHECKING:
    from schemas.roles import RoleRead

class PermissionRead(BaseModel):
    id: int
    name: str
    role: List[RoleRead]
class PermissionCreate(BaseModel):
    name: str