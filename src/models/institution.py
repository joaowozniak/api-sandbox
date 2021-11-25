from pydantic import BaseModel


class Institution(BaseModel):
    id: str
    name: str
