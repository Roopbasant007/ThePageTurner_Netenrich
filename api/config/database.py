from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine

DB_URI = "mysql+pymysql://root@localhost:3306/tptdb"
engine = create_engine(DB_URI)
conn = engine.connect()
Session = sessionmaker(bind=engine)


Base = declarative_base()