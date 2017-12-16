
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from pykbdb import Base

class Tag(Base):
    __tablename__ = 'tags'
    foreign_id = Column(String, index=True, primary_key=True)
    type = Column(String, primary_key=True)
    tag = Column(String, index=True, primary_key=True)
