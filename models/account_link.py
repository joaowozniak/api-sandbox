from pydantic import BaseModel
from typing import List

class Account_Link(BaseModel):
    balances: str
    details: str
    self: str
    transactions: str

    def show_details(self):
        return {"account": self.self, "self": self.details}

    def show_balances(self):
        return {"account": self.self, "self": self.balances}        


