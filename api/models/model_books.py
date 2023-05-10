from sqlalchemy import Integer, Boolean, String, Column
from api.config.database import Base

class Book_Model(Base):
    __tablename__ = "books"
    
    title = Column(String(150), index=True)
    author = Column(String(50), index=True)
    genre = Column(String(30), index=True)
    year_of_publication = Column(Integer,  index=True)
    ISBN = Column(String(17), primary_key=True, index=True)
    status = Column(Boolean, default = 0)

