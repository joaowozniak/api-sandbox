from pydantic import BaseModel
from typing import List

class Account_Link(BaseModel):
    balances: str
    details: str
    self: str
    transactions: str
    account: str 