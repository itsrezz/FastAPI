from __future__ import annotations
from pydantic import BaseModel, EmailStr
from typing import Dict, ClassVar


class Session(BaseModel):
    session_id: int
    username: str
    time: datetime.now()