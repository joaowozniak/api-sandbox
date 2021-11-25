from pydantic import BaseModel
from ..models.institution import Institution
from ..models.account import Account
from ..models.transaction_link import Transaction_Link
from ..models.description import Description
import datetime


class Transaction(BaseModel):
    account_id: str
    amount: int
    date: str
    description: Description
    id: str
    links: Transaction_Link
    running_balance: int
    status: str
    type: str
