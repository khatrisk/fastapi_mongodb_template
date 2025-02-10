"""
User Models
"""
import pytz
from datetime import datetime
from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr, ConfigDict

from models.thing_model import MyThing



india_tz = pytz.timezone("Asia/Calcutta")


class ImageBase(BaseModel):
    public_id: str
    uri: str

class UserBase(Document):
    """User database representation"""
    model_config = ConfigDict(extra='allow') 
    
    first_name: Optional[str] | None = None
    last_name: Optional[str] | None = None
    created_at: Optional[datetime] = datetime.now(india_tz)
    disabled: bool = False
    email: Optional[EmailStr] | None = None
    username: Optional[str] | None = None
    password_hash: Optional[str] | None = None
    things: Optional[List[Link[MyThing]]] | None = []

    class Settings:
        name = "Users"
        

    
    
class UserIn(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserOut(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: dict
    email: EmailStr
    username: str
    created_at: datetime
    things: List[Link[MyThing]]


class UserUpdate(BaseModel):
    """User database representation"""
    model_config = ConfigDict(extra='allow')
    
    first_name: Optional[str] | None = None
    last_name: Optional[str] | None = None
    email: Optional[EmailStr] | None = None
    username: Optional[str] | None = None
