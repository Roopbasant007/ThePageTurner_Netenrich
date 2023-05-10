from sqlalchemy import Integer, String, Column
from api.config.database import Base

class Student_Model(Base):
    __tablename__ = "students"
    rollno = Column(String(8), primary_key=True, index=True, nullable=False)
    name = Column(String(50), index=True, nullable=False )
    course = Column(String(50), index=True, nullable=False)
    dept = Column(String(50), index=True, nullable=False)
    year_of_admission = Column(Integer, index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(64), index=True, nullable=False)










