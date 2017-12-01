import bcrypt

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pykbdb import Base

# Make a user object.
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    passwordhash = Column(String)

    def setpw(password):
        self.passwordhash = bcrypt.hashpw(password, bcrypt.gensalt())

    def checkpw(password):
        return bcrypt.checkpw(password, self.passwordhash)
