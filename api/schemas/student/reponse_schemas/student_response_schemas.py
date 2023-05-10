from typing import List, Optional
from pydantic import BaseModel

class SystemUser(BaseModel):
    rollno: str
    password: str

    class config:
        orm_mode = True

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

    class config:
        orm_mode = True

class RecommendedFriendDetailsSchema(BaseModel):
    rollno = str
    name = str
    course = str
    dept = str
    year_of_admission = int
    email = str

    class Config:
        orm_mode = True