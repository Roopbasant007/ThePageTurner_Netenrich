from pydantic import BaseModel

class ConnectionRequestSchema(BaseModel):
    sender: str
    receiver: str
    
    class Config:
        orm_mode = True


class ConnectionCreationSchema(ConnectionRequestSchema):
    status : str

    class Config:
        orm_mode = True