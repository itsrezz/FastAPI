from __future__ import annotations
from pydantic import BaseModel, EmailStr
from typing import Dict, ClassVar


class Post(BaseModel):
    title: str
    content: str
    author: str
    id: int
    posts: ClassVar[Dict[str,Post]]