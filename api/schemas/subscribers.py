from pydantic import BaseModel, DirectoryPath, PastDatetime

from modules.auth.schemas.user import UserRead


class Subscriber(BaseModel):
    subscriber: UserRead
    subscriben: UserRead