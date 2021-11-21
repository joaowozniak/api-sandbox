from pydantic import BaseModel
from models.counterparty import Counterparty

class Description(BaseModel):
    category: str
    counterparty: Counterparty
    processing_status: str