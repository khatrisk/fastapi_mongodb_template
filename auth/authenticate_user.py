from models.user_model import UserBase
from auth.verify_password import verify_password


async def get_user_by_username(username):
    user_data = await UserBase.find_one(UserBase.username == username)
    if not user_data:
        return False
    return user_data


async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user
