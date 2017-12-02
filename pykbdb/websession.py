from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pykbdb import Base

# Make a user object.
class WebSession(Base):
    __tablename__ = 'sessions'
    authorization = Column(String, primary_key=True)
    user_name = Column(String, index=True)
    expiration = Column(DateTime)
