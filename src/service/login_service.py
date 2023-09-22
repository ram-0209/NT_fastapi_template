"""Login Service"""
import random
import string
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.exception.user_exception import get_user_exception
from src.models.user_model import User
from src.repository import user_repository

SECRET = "ipxktny"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    """get_password_hash

    Args:
        password (_type_): password

    Returns:
        _type_: hashed password
    """
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    """verify_password

    Args:
        plain_password (_type_): plain password
        hashed_password (bool): hashed password

    Returns:
        _type_: Bool
    """
    return bcrypt_context.verify(plain_password, hashed_password)


def get_user(username: str, session):
    """get_user

    Args:
        username (str): username
        session (_type_): database session

    Returns:
        _type_: user
    """
    user = user_repository.get_user_by_username_db(
        username["preferred_username"], session
    )
    if user and user[0].is_active:
        return {"status": True, "user": user[0]}
    elif not user:
        token_create_user(username, session)
    return {"status": False, "user": False}


# Make same as like other function the query need to call from repository
def authenticated_user(username: str, password: str, session):
    """authenticate_user

    Args:
        username (str): username
        password (str): password
        session (_type_): Database Session

    Returns:
        _type_: authenticated user
    """
    if user := user_repository.get_user_by_username_db(username, session):
        return user[0] if verify_password(password, user[0].password) else False
    else:
        return False


def create_access_token(
    username: str, user_id: int, expires_delta: Optional[timedelta] = None
):
    """Create access Token

    Args:
        username (str): username
        user_id (int): Id of the user
        expires_delta (Optional[timedelta], optional): Defaults to None.

    Returns:
        _type_: JWT Token
    """
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_bearer)):
    """Get Current User

    Args:
        token (str, optional): _description_. Defaults to Depends(oauth2_bearer).

    Raises:
        get_user_exception: user does not exist
        get_user_exception: JWT token error

    Returns:
        _type_: user
    """
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError as e:
        raise get_user_exception() from e


def check_user_valid(token: str):
    """Check if user is valid

    Args:
        token (str): JWT token

    Raises:
        get_user_exception: JWT token invalid

    Returns:
        _type_: user is not None
    """
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        return username is not None and user_id is not None
    except JWTError as e:
        raise get_user_exception() from e


def get_random_password(length):
    """Get Random Password

    Args:
        length (_type_): length of password

    Returns:
        _type_: password
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))


def token_create_user(data_obj, session):
    """Token Create User

    Args:
        data_obj (_type_): data
        session (_type_): database session

    Returns:
        _type_: user
    """
    random_password = get_random_password(length=8)
    new_user = User(
        username=data_obj["preferred_username"],
        email=data_obj["preferred_username"],
        first_name=data_obj["name"],
        last_name=data_obj["name"],
        password=get_password_hash(random_password),
        is_active=True,
    )
    session.add(new_user)
    session.commit()
    return User
