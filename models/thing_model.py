"""
User Models
"""
import pytz
from datetime import datetime
from typing import Optional

from beanie import Document, Link
from pydantic import BaseModel, EmailStr, ConfigDict


india_tz = pytz.timezone("Asia/Calcutta")


class Category(BaseModel):
    category_name: str


class MyThingIn(BaseModel):
    thing_name: str
    thing_description: Optional[str] | None = None
    category: Category


class MyThingOut(BaseModel):
    thing_name: str
    owner: str
    category: Category


class MyThing(Document):
    """User database representation"""

    model_config = ConfigDict(extra="allow")

    thing_name: str | None = None
    thing_description: Optional[str] | None = None
    created_at: datetime = datetime.now(india_tz)
    owner: str | None = None
    category: Category

    class Settings:
        name = "Things"
