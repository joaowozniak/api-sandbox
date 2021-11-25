from pydantic import BaseModel
from typing import List, Optional
from ..models.institution import Institution
from ..models.account_link import Account_Link
from ..models.routing_number import Routing_Number


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

    def show_accounts(self):
        return {
            "currency": self.currency,
            "enrollment_id": self.enrollment_id,
            "id": self.account_id,
            "institution": self.institution,
            "last_four": self.last_four,
            "links": self.links,
            "name": self.name,
            "subtype": self.subtype,
            "type": self.type,
        }

    def show_accounts_details(self):
        return {
            "account_id": self.account_id,
            "account_number": self.account_number,
            "links": self.links.show_details(),
            "routing_numbers": self.routing_number,
        }

    def show_accounts_balances(self):
        return {
            "account_id": self.account_id,
            "available": self.available,
            "ledger": self.ledger,
            "links": self.links.show_balances(),
        }
