from pydantic import BaseModel
from typing import List, Optional
from models.institution import Institution
from models.account_link import Account_Link

class Account(BaseModel):
    currency: str
    enrollment_id: str
    account_id: str
    account_number: str
    institution: Institution
    last_four: str
    links: Account_Link
    name: str
    subtype: str
    type: str

def get_all_account_names():
    names = ["My Checking", "Jimmy Carter", "Ronald Reagan", "George H. W. Bush", "Bill Clinton", "George W. Bush", "Barack Obama", "Donald Trump"]
    return names


    