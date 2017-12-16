# The database ORM stuff for pykb.
import sqlalchemy

print("SQLALCHEMY VERSION "+sqlalchemy.__version__)

from sqlalchemy import create_engine
# from sqlalchemy import Column
# from sqlalchemy import Integer
# from sqlalchemy import String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
from pykbdb.user import User
from pykbdb.websession import WebSession
from pykbdb.blob import Blob
from pykbdb.tag import Tag

# Create an engine everyone can use.
engine = create_engine('sqlite:///db.sqlite3', echo=True)

# Migrate the database.
Base.metadata.create_all(engine)

# How do we make sessions?
Session = sessionmaker(bind=engine)

# session = Session()
# session.add(User(name='hi'))
# print(session.query(User).filter_by(name='ed').first())
# session.close()
