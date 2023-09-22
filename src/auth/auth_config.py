"""JWT authentication"""
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.exception.user_exception import get_user_exception
from src.service.login_service import check_user_valid


def verify_jwt(jwtoken: str):
    """Verify JWT

    Args:
        jwtoken (str): JWT Token

    Returns:
        _type_: bool(payload)
    """
    try:
        payload = check_user_valid(jwtoken)
    except Exception:
        payload = None
    return bool(payload)


class JWTBearer(HTTPBearer):
    """JWT Authentication class"""

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if not credentials:
            raise get_user_exception()
        if credentials.scheme != "Bearer":
            raise get_user_exception()
        if not verify_jwt(credentials.credentials):
            raise get_user_exception()
        return credentials.credentials
