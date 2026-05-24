from pydantic import BaseModel, DirectoryPath, PastDatetime

from auth.schemas.user import UserRead


class Vidos(BaseModel):
    subscriber: UserRead
    subscriben: UserRead