from pydantic import BaseModel


class Transaction_Link(BaseModel):
    account: str
    self: str

