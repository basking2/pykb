
from unittest import TestCase

import pykbdb
from pykbdb import Blob
from pykbdb import Tag

import struct

class DbTest(TestCase):
    def test_readwriteblob_simple(self):
        sess = pykbdb.Session()
        b = Blob(
            id = "title",
            title="title",
            contenttype="text/plain",
            content="hi".encode())
        sess.query(Blob).filter(Blob.id == b.id).delete()
        sess.add(b)
        sess.commit()
        sess.close()

    def test_blobtagging(self):
        sess = pykbdb.Session()
        try:
            b = Blob(id='title')
            b.tags = [ Tag(foreign_id=b.id, type="blobl", tag = "hi") ]

            sess.query(Blob).filter(Blob.id == b.id).delete()
            sess.add(b)
        finally:
            sess.close()
