from __future__ import annotations
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Dict
from enum import Enum
# from uuid import uuid4, UUID

#Enum:Enumeration
class UserRole(str,Enum):
    REGULAR = "regular"
    ADMIN = "admin"

class TokkenData(BaseModel):
    username:str
    # role:str


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole=UserRole.REGULAR.value

# class UserWrite(BaseUser):

    # _id: UUID = Field(default_factory=uuid4)
    
# class UserShow(BaseUser):
    # id: Field(default_factory=get_id)

    # def get_id(self)->UUID:
    #     return self._id
    # @validator('username')
    # def unique_username(cls, username):
    #     if username in cls.users:
    #         raise ValueError('Username is already exist!')
    #     return username


