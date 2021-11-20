from fastapi import HTTPException
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param

from starlette.requests import Request
from typing import Optional

class BasicAuth (SecurityBase):
    def __init__(self, scheme_name: str = None):
        self.scheme_name = scheme_name

    def __call__(self, request: Request) -> Optional[str]:
        authorized: str = request.headers.get("Authorization")        
        scheme, param = get_authorization_scheme_param(authorized)
        print(authorized)
        print(param)
        print(scheme)
        if not authorized or scheme.lower() != "basic":
            raise HTTPException(
                status_code=401, 
                detail="Not authorized", 
                headers={"WWW-Authenticate" : "Basic"}
            )   

        token = "test_" + param     
        return token