from pydantic import BaseModel, DirectoryPath, PastDatetime, FilePath


class Vidos(BaseModel):
    id: int
    name: str
    vidos_path: FilePath
    length: int
    date: PastDatetime
    extension: str

class VidosCreate(BaseModel):
    name: str
    vidos_path: DirectoryPath