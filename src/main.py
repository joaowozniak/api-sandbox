import secrets, base64

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import Response

from starlette.requests import Request
from starlette.responses import RedirectResponse
from typing import Optional

class BasicAuth (SecurityBase):
    def __init__(self, scheme_name: str = None):
        self.scheme_name = scheme_name

    def __call__(self, request: Request) -> Optional[str]:
        authorized: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorized)
        if not authorized or scheme.lower() != "basic":
            raise HTTPException(
                status_code=401, 
                detail="Not authorized", 
                headers={"WWW-Authenticate" : "Basic"}
            )
        return param
        

sandbox = FastAPI()

basic_auth = BasicAuth()


def check_username_format(username: str):
    if username.startswith("test_"):        
        return username
    else:
        return ("FALSE_"+username)


def get_current_user(token: str = Depends(basic_auth)) -> str:
    decoded = base64.b64decode(token).decode("ascii")
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
def root(auth: BasicAuth = Depends(basic_auth)): 
    if not auth:
        response = Response(
            status_code = 401, 
            headers={"WWW-Authenticate": "Basic"}
        )
        return response
    
    token = get_current_user(auth)
    response = RedirectResponse(url="/welcome")
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        domain="localtest.me",
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response

@sandbox.get("/welcome")
def welcome(current_user: str = Depends(get_current_user)):
    return "WELCOME!"
