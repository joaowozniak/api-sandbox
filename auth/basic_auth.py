import secrets, base64
from fastapi import HTTPException, Depends
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from typing import Optional, Dict


class BasicAuth(SecurityBase):
    def __init__(self, scheme_name: str = None):
        self.scheme_name = scheme_name

    def __call__(self, request: Request) -> Dict[str, bool]:
        authorized: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorized)

        if not authorized or scheme.lower() != "basic":
            raise HTTPException(
                status_code=401,
                detail="Not authorized",
                headers={"WWW-Authenticate": "Basic"},
            )

        has_access, has_more_account = verify_user(param)

        token = "test_" + has_access
        return {"token": token, "has_more_account": has_more_account}


def check_username(username: str) -> Dict[str, bool]:
    if (
        username.startswith("user_multiple_")
        and username[-5:].isdigit()
        and len(username) == 19
    ):
        return {"name": username, "has_more_account": True}

    elif (
        username.startswith("user_") and username[-5:].isdigit() and len(username) == 10
    ):
        return {"name": username, "has_more_account": False}

    else:
        return {"name": "_" + username, "has_more_account": False}


def verify_user(param: str) -> (str, bool):

    decoded = base64.b64decode(param).decode("ascii")
    username, _, password = decoded.partition(":")
    has_more_account = check_username(username)["has_more_account"]

    correct_username = secrets.compare_digest(
        username, check_username(username)["name"]
    )
    correct_password = secrets.compare_digest(password, "")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Credentials not valid",
            headers={"WWW-Authenticate": "Basic"},
        )

    return (param, has_more_account)
