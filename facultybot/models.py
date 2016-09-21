# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, Integer
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///taizan.sqlite3')
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Speech(Base):
    __tablename__ = 'speech'

    id = Column(Integer, primary_key=True)
    speech = Column(Text)

def create_table():
    Base.metadata.create_all(engine)


