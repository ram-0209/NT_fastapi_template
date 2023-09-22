"""User Exceptions Structure"""
from fastapi import HTTPException, status


def raise_item_can_not_be_found_exception():
    """Item cannot be Found Exception

    Returns:
        _type_: HTTPException
    """
    return HTTPException(
        status_code=404,
        detail="Item not found",
    )


def get_user_exception():
    """Unauthorized User Exception

    Returns:
        _type_: HTTPException
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


def token_exception():
    """Token Mismatch Exception

    Returns:
        _type_: HTTPException
    """
    token_mismatch_exception = HTTPException(
        status_code=500,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_mismatch_exception
