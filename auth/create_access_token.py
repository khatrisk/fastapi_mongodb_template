from datetime import datetime, timedelta
from jose import jwt
from dotenv import dotenv_values

env = dotenv_values(".env")
SECRET_KEY = env["SECRET_KEY"]
ALGORITHM = env["ALGORITHM"]


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
