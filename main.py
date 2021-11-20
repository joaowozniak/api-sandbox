import secrets, base64

from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi.security import HTTPBasic
from fastapi.security.base import SecurityBase
from fastapi.openapi.models import Response

from starlette.requests import Request
from starlette.responses import RedirectResponse
from typing import Optional, List
from auth.basicAuth import BasicAuth, check_username_format

from contexts.accounts import *

sandbox = FastAPI()

basic_auth = BasicAuth()

def get_current_user(token: str = Depends(basic_auth)) -> (str, int):
    decoded = base64.b64decode(token[5:]).decode("ascii")
    username, _, password = decoded.partition(":")
    flag = check_username_format(username)[1]
    print(flag)
    correct_username = secrets.compare_digest(username, check_username_format(username)[0])
    correct_password = secrets.compare_digest(password, "")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401, 
            detail="Not authorized", 
            headers={"WWW-Authenticate" : "Basic"}
        )  
    return (token, flag)

    
@sandbox.get("/")
def welcome():
    return "Hello! Navigate to /login to log in."


@sandbox.get("/login")
def welcome(current_user: (str, int) = Depends(get_current_user)):       
    return "WELCOME! You can navigate to: /accounts to check your accounts. /accounts/:id to check a specific account"


@sandbox.get("/accounts")
def get_accounts(current_user: (str, int) = Depends(get_current_user)): 
    accounts = generate_accounts(current_user[0], current_user[1])
    return accounts

@sandbox.get("/accounts/{idx}")
def get_accounts_by_id(current_user: (str, int) = Depends(get_current_user), idx: str = None): 
    accounts = generate_accounts(current_user[0], current_user[1])
    acc = get_account_by_id(accounts, idx)
    return acc
