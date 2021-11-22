import secrets, base64

from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi.security import HTTPBasic
from fastapi.security.base import SecurityBase
from fastapi.openapi.models import Response

from starlette.requests import Request
from starlette.responses import RedirectResponse
from typing import Optional, List
from auth.basic_auth import BasicAuth

from controllers.accounts import *
from controllers.transactions import *


sandbox = FastAPI()

basic_auth = BasicAuth()


def get_current_user(token: str = Depends(basic_auth)) -> (str, int):
    return token


@sandbox.get("/")
def welcome():
    return "Hello, navigate to /login to log in."


@sandbox.get("/login")
def login(current_user: (str, int) = Depends(get_current_user)):
    return "Welcome, you're logged in."


@sandbox.get("/accounts")
def get_accounts(current_user: (str, int) = Depends(get_current_user)):
    accounts = generate_accounts(current_user[0], current_user[1])
    accounts_formatted = [acc.show_accounts() for acc in accounts]
    return accounts_formatted


@sandbox.get("/accounts/{idx}")
def get_accounts_by_id(
    current_user: (str, int) = Depends(get_current_user), idx: str = None
):
    accounts = generate_accounts(current_user[0], current_user[1])
    account_by_id = get_account_by_id(accounts, idx)
    account_formatted = account_by_id.show_accounts()
    return account_formatted


@sandbox.get("/accounts/{idx}/details")
def get_accounts_by_id(
    current_user: (str, int) = Depends(get_current_user), idx: str = None
):

    accounts = generate_accounts(current_user[0], current_user[1])
    account_by_id = get_account_by_id(accounts, idx)
    account_formatted = account_by_id.show_accounts_details()
    return account_formatted


@sandbox.get("/accounts/{idx}/balances")
def get_accounts_by_id(
    current_user: (str, int) = Depends(get_current_user), idx: str = None
):
    accounts = generate_accounts(current_user[0], current_user[1])
    account_by_id = get_account_by_id(accounts, idx)
    account_formatted = account_by_id.show_accounts_balances()
    return account_formatted


@sandbox.get("/accounts/{idx}/transactions")
def get_accounts_by_id(
    current_user: (str, int) = Depends(get_current_user), idx: str = None
):
    accounts = generate_accounts(current_user[0], current_user[1])
    account_by_id = get_account_by_id(accounts, idx)
    trans = generate_data_from_acc(account_by_id)
    return trans
