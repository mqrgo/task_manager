import datetime

from sqlalchemy import Column, Integer, String, LargeBinary, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    password = Column(LargeBinary, nullable=False)
    email = Column(String, nullable=False)
    # tasks = relationship('Task')



class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer(), primary_key=True)
    topic = Column(LargeBinary(), nullable=False)
    date = Column(DateTime(), default=datetime.datetime.now())
    is_done = Column(Boolean(), nullable=False, default=False)
    user_id = Column(Integer(), ForeignKey('users.id'))
    user = relationship('User')



metadata = Base.metadata
