import sqlalchemy.exc as exc
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Data(Base):
    __tablename__ = "data"

    id = Column('id', Integer, primary_key=True)

        