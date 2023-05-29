from __future__ import annotations
from pydantic import BaseModel, EmailStr
from typing import Dict, ClassVar
from datetime import datetime
from uuid import uuid4


class Session(BaseModel):
    session_id: str = str(uuid4())
    username: str
    time:datetime = datetime.now()