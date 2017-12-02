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
    username = Column(String, primary_key=True)
    authorization = Column(String, unique=True)
    expiration = Column(DateTime)

    def setpw(password):
        self.passwordhash = bcrypt.hashpw(password, bcrypt.gensalt())

    def checkpw(password):
        return bcrypt.checkpw(password, self.passwordhash)
