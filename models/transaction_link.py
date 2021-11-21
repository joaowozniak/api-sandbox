from pydantic import BaseModel

class Transaction_Link(BaseModel):
    account: str
    self: str


def fill_links(base_link: str, acc: str):

    return Transaction_Link(
        account = (base_link + acc + "/account"),
        self = (base_link + acc)
    )    