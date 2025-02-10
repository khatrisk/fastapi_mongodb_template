from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password) -> str:
    """Makes hash of a plain-text password"""
    return pwd_context.hash(password)
