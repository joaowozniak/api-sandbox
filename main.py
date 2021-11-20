import secrets, base64

from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi.security import HTTPBasic
from fastapi.security.base import SecurityBase
from fastapi.openapi.models import Response

from starlette.requests import Request
from starlette.responses import RedirectResponse
from typing import Optional, List
from auth.basicAuth import BasicAuth

from contexts.accounts import from_token

sandbox = FastAPI()

basic_auth = BasicAuth()


def check_username_format(username: str):
    if username.startswith("user_"):        
        return username
    else:
        return ("_"+username)


def get_current_user(token: str = Depends(basic_auth)) -> str:
    decoded = base64.b64decode(token[5:]).decode("ascii")
    username, _, password = decoded.partition(":")

    correct_username = secrets.compare_digest(username, check_username_format(username))
    correct_password = secrets.compare_digest(password, "")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401, 
            detail="Not authorized", 
            headers={"WWW-Authenticate" : "Basic"}
        )  
    return token

    
@sandbox.get("/")
def welcome():
    return "Hello! Navigate to /login to log in."

@sandbox.get("/login")
def welcome(current_user: str = Depends(get_current_user)):
    print(current_user)    
    return "WELCOME! You can navigate to: /accounts to check your accounts. /accounts/:id to check a specific account"


@sandbox.get("/accounts")
def get_accounts(current_user: str = Depends(get_current_user)): 
    account = from_token(current_user)
    return {
        "currency":account.currency, 
        "institution":account.institution.id}


