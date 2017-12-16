
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import BLOB
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from pykbdb import Base

# Make a user object.
class Blob(Base):
    __tablename__ = 'blobs'
    id = Column(String, primary_key=True)
    title = Column(String, index=True)
    content = Column(BLOB)
    owner = Column(String)
    contenttype = Column(String)
    creation = Column(DateTime)
    modification = Column(DateTime)
    expiration = Column(DateTime)
    tags = relationship("BlobTag", cascade="all, delete, delete-orphan")

    def addtag(self, tag):
        if self.tags == None:
            self.tags = [ BlobTag(blobs_id = self.id, tag = tag) ]
        else:
            self.tags.append(BlobTag(blobs_id = self.id, tag = tag))

    def deltag(self, tag):
        if self.tags != None:
            i = 0
            while i < len(self.tags):
                if self.tags[i].tag == tag:
                    del(self.tags[i])
                i += 1

class BlobTag(Base):
    __tablename__ = 'blob_tags'
    blobs_id = Column(String, ForeignKey('blobs.id'), primary_key = True, index = True)
    tag = Column(String, primary_key = True, index = True)
