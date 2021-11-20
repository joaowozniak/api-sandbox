from fastapi import HTTPException, Depends
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param

from starlette.requests import Request
from typing import Optional
import secrets, base64

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

        token = "test_" + param     
        return token

def check_username_format(username: str) -> (str, int):
    if username.startswith("user_multiple_"): 
        
        return (username, 1)
    
    elif username.startswith("user_"):      
        return (username, 0)      
        
    else:
        return ("_"+username, 0)
