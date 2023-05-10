from sqlalchemy import Integer, Boolean, String, Column
from api.config.database import Base


class Connection_Model(Base):
    __tablename__ = "connection"
    
    connid = Column(Integer, primary_key = True, autoincrement = True , nullable = False )
    sender = Column(String(10))
    receiver = Column(String(10))
    status = Column(String(20))




    

