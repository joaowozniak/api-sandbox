from pydantic import BaseModel

class Routing_Number(BaseModel):
    ach: str
