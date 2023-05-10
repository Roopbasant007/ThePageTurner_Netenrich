from typing import List, Optional
from pydantic import BaseModel, EmailStr 

    
#classSchema has been inherited from AdminSchema 
class CreateAdminSchema(BaseModel):
    name: str
    year_of_joining: int
    email: EmailStr
    password: str 

    class Config:
        orm_mode = True
            

# schema for login request 
class LoginRequestSchema(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


# schema for book adding book 

class AddBookSchema(BaseModel):
    title : str
    author : str
    genre : str
    year_of_publication : int
    ISBN : str
   
    class Config:
        orm_mode = True