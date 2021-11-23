import hashlib
from typing import List, Optional
from models.account import Account
from models.account_link import Account_Link
from models.institution import Institution
from controllers.institutions import *
from controllers.routing_numbers import *


def get_all_account_names():
    names = [
        "My Checking",
        "Jimmy Carter",
        "Ronald Reagan",
        "George H. W. Bush",
        "Bill Clinton",
        "George W. Bush",
        "Barack Obama",
        "Donald Trump",
    ]
    return names

def encode_with_alfanumeric(token: str, type: str) -> str:
    if type == "enr":
        encoded = str(hashlib.sha256(token.encode()).hexdigest())[-22:]
    
    elif type == "id":
        encoded = str(hashlib.md5(token.encode()).hexdigest())[-22:]

    return encoded

def pseudo_random_from_token(token: str, type: str) -> str:
    if type == "inst" or type == "name":
        prandom = (abs(hash(str(hashlib.md5(token.encode()).hexdigest()))))

    elif type == "acc_num":
        prandom = str(abs(hash(token)) % (10 ** 13))[-10:]
    return prandom

def pseudo_random_starting_available(account_id: str) -> int:
    amounts = [i for i in range(10, 10000)]
    amount = amounts[abs(hash(account_id)) % len(amounts)]
    return amount

def fill_links(account_id: str) -> Account_Link:

    base_link = "http://localhost:8000/accounts/"

    return Account_Link(
        balances=(base_link + account_id + "/balances"),
        details=(base_link + account_id + "/details"),
        self=(base_link + account_id),
        transactions=(base_link + account_id + "/transactions")
    )

def fill_data_from_token(token: str) -> Account:

    enrollment_id = "enr_" + encode_with_alfanumeric(token, "enr")
    account_id = "acc_" + encode_with_alfanumeric(token, "id")  
    
    institutions = get_all_institutions()
    institution = institutions[pseudo_random_from_token(token, "inst") % len(institutions)]
    
    acc_num = pseudo_random_from_token(token, "acc_num")

    last_four = acc_num[-4:]

    names = get_all_account_names()
    name = names[pseudo_random_from_token(token, "name") % len(names)]

    links = fill_links(account_id)

    routing_number = get_routingnum_by_inst(institution.id)

    acc_key = account_id[4:]

    available_balance = pseudo_random_starting_available(acc_key)
    ledger_balance = pseudo_random_starting_available(acc_key)

    return Account(
        currency="USD",
        enrollment_id=enrollment_id,
        account_id=account_id,
        institution=institution,
        account_number=acc_num,
        last_four=last_four,
        links=links,
        routing_number=routing_number,
        name=name,
        subtype="checking",
        type="depository",
        available=available_balance,
        ledger=ledger_balance
    )


def generate_accounts(token: str, only_one_account: bool) -> List[Account]:
    
    account_one = fill_data_from_token(token)

    if only_one_account == False:
        return [account_one]

    else:       
        token_acc2 = token[::-1]
        account_two = fill_data_from_token(token_acc2)

    return [account_one, account_two]


def get_account_by_id(accounts: List[Account], id: str) -> Account:

    for account in accounts:
        if id == account.account_id:
            return account 
    return None       
