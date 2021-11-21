from pydantic import BaseModel
from models.institution import Institution
from models.account import Account
from models.transaction_link import Transaction_Link
from models.description import Description
import datetime

class Transaction(BaseModel):
    account_id: str
    amount: float
    date: str
    description: Description
    processing_status: str
    id: str
    links: Transaction_Link
    running_balance: float
    status: str
    type: str