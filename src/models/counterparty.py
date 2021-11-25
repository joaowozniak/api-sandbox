from pydantic import BaseModel


class Counterparty(BaseModel):
    name: str
    type: str
