from pydantic import BaseModel
from typing import List

class Account_Link(BaseModel):
    balances: str
    details: str
    self: str
    transactions: str

def fill_links(base_link: str, acc: str) -> Account_Link:

    return Account_Link(
        balances = (base_link + acc + "/balances"),
        details = (base_link + acc + "/details"),
        self = (base_link + acc),
        transactions = (base_link + acc + "/transactions")       
    )        