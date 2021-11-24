from fastapi import Depends, HTTPException, FastAPI
from fastapi.security import HTTPBasic
from fastapi.security.base import SecurityBase
from fastapi.openapi.models import Response

from starlette.requests import Request
from starlette.responses import RedirectResponse
from typing import Optional, List, Dict
from auth.basic_auth import BasicAuth

from controllers.accounts import generate_accounts, get_account_by_id
from controllers.transactions import generate_transactions, get_transaction_by_id


sandbox = FastAPI()

basic_auth = BasicAuth()

print("Starting app...")


def get_current_user(
    token_dict: Dict[str, bool] = Depends(basic_auth)
) -> Dict[str, bool]:
    return token_dict


@sandbox.get("/")
def welcome():
    return "Hello. Log in with user_XXXXX where X is digit. user_multiple_XXXXX for user with multiple accounts. Password empty."


@sandbox.get("/accounts")
def get_accounts(current_user: Dict[str, bool] = Depends(get_current_user)):
    accounts = generate_accounts(
        current_user["token"], current_user["has_more_account"]
    )
    accounts_formatted = [acc.show_accounts() for acc in accounts]
    return accounts_formatted


@sandbox.get("/accounts/{idx}")
def get_accounts_by_id(
    current_user: Dict[str, bool] = Depends(get_current_user), idx: str = None
):
    accounts = generate_accounts(
        current_user["token"], current_user["has_more_account"]
    )
    account_by_id = get_account_by_id(accounts, idx)
    account_formatted = account_by_id.show_accounts()
    return account_formatted


@sandbox.get("/accounts/{idx}/details")
def get_accounts_details(
    current_user: Dict[str, bool] = Depends(get_current_user), idx: str = None
):

    accounts = generate_accounts(
        current_user["token"], current_user["has_more_account"]
    )
    account_by_id = get_account_by_id(accounts, idx)
    if account_by_id is None:
        return "Can't"
    account_formatted = account_by_id.show_accounts_details()
    return account_formatted


@sandbox.get("/accounts/{idx}/balances")
def get_accounts_balances(
    current_user: Dict[str, int] = Depends(get_current_user), idx: str = None
):
    accounts = generate_accounts(
        current_user["token"], current_user["has_more_account"]
    )
    account_by_id = get_account_by_id(accounts, idx)
    if account_by_id is None:
        return "Can't"
    account_formatted = account_by_id.show_accounts_balances()
    return account_formatted


@sandbox.get("/accounts/{idx}/transactions")
def get_transactions(
    current_user: Dict[str, int] = Depends(get_current_user), idx: str = None
):
    accounts = generate_accounts(
        current_user["token"], current_user["has_more_account"]
    )
    account_by_id = get_account_by_id(accounts, idx)
    if account_by_id is None:
        return "Can't"
    transactions = generate_transactions(account_by_id)
    return transactions


@sandbox.get("/accounts/{idx}/transactions/{idt}")
def get_transactions_by_id(
    current_user: Dict[str, int] = Depends(get_current_user),
    idx: str = None,
    idt: str = None,
):
    accounts = generate_accounts(
        current_user["token"], current_user["has_more_account"]
    )
    account_by_id = get_account_by_id(accounts, idx)
    if account_by_id is None:
        return "Can't"

    transactions = generate_transactions(account_by_id)
    transaction_by_id = get_transaction_by_id(transactions, idt)
    if transaction_by_id is None:
        return "Can't"

    return transaction_by_id
