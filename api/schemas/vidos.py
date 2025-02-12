from pydantic import BaseModel, DirectoryPath, PastDatetime
class Vidos(BaseModel):
    name: str
    vidos_path: DirectoryPath
    length: str
    date: PastDatetime
