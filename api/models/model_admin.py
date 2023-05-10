from sqlalchemy import Integer, String, Column
from api.config.database import Base

class Admin_Model(Base):
    __tablename__ = "admins"
    name = Column(String(50), index=True, nullable=False )
    year_of_joining = Column(Integer, index=True, nullable=False)
    email = Column(String(50), unique=True, primary_key = True, index=True, nullable=False)
    password = Column(String(64), index=True, nullable=False)