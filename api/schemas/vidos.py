from pydantic import BaseModel, DirectoryPath, PastDatetime
class Vidos(BaseModel):
    id: int
    name: str
    vidos_path: DirectoryPath
    length: str
    date: PastDatetime
    extension: str

class VidosCreate(BaseModel):
    name: str
    vidos_path: DirectoryPath