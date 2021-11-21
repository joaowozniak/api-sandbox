from pydantic import BaseModel
from typing import List, Optional
from models.institution import Institution
from models.account_link import Account_Link
from models.routing_number import Routing_Number

class Account(BaseModel):
    currency: str
    enrollment_id: str
    account_id: str
    account_number: str
    institution: Institution
    last_four: str
    links: Account_Link
    routing_number: Routing_Number
    name: str
    subtype: str
    type: str
    available: float
    ledger: float
