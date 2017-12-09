
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import BLOB

from pykbdb import Base

# Make a user object.
class Blob(Base):
    __tablename__ = 'blobs'
    id = Column(String, primary_key=True)
    tag_set = Column(String, unique=True)
    title = Column(String, index=True)
    content = Column(BLOB)
    owner = Column(String)
    contenttype = Column(String)

    creation = Column(DateTime)
    modification = Column(DateTime)
    expiration = Column(DateTime)
