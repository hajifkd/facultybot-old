# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///faculty.sqlite3')
Base = declarative_base()
Session = sessionmaker(bind=engine)

class NickName(Base):
    __tablename__ = 'nickname'

    id = Column(Integer, primary_key=True)
    nickname = Column(Text, unique=True)
    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship('Faculty')

class Faculty(Base):
    __tablename__ = 'faculty'

    id = Column(Integer, primary_key=True)
    nicknames = relationship('NickName')
    speeches = relationship('Speech')

class Speech(Base):
    __tablename__ = 'speech'

    id = Column(Integer, primary_key=True)
    speech = Column(Text)
    faculty_id = Column(Integer, ForeignKey('faculty.id'))
    faculty = relationship('Faculty')

def create_table():
    Base.metadata.create_all(engine)


