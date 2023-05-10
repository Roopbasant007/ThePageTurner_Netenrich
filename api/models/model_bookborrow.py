from sqlalchemy import Integer, String, Column
from api.config.database import Base


class Bookborrow_Model(Base):
    __tablename__ = "bookborrow"
    
    borrowid = Column(Integer, primary_key = True, autoincrement = True , nullable = False)
    borrowerid = Column(String(10))
    ISBN = Column(String(17))
    status = Column(String(20))

    
