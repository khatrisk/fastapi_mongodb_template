"""
Current user dependency
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from models.token_models import TokenData
from models.user_model import UserBase

from auth.authenticate_user import get_user_by_username

from dotenv import dotenv_values

env = dotenv_values(".env")
SECRET_KEY = env["SECRET_KEY"]
ALGORITHM = env["ALGORITHM"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: UserBase = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserBase = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
