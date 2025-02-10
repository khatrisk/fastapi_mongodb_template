from pydantic import BaseModel
from typing import Optional

class Message(BaseModel):
    message: Optional[str] | None = "Sample message"