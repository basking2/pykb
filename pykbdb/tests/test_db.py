
from unittest import TestCase

import pykbdb
from pykbdb import Blob
from pykbdb import BlobTag

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
            b = sess.query(Blob).get('title')
            if b != None:
                sess.delete(b)
                sess.commit()

            b = Blob(id='title')
            b.tags = []
            b.tags.append(BlobTag(blobs_id=b.id, tag = "hi"))
            b.addtag('bye')
            b.deltag('bye')
            sess.add(b)
            sess.commit()
            b = sess.query(Blob).filter(Blob.id == b.id)[0]
            self.assertEqual('hi', b.tags[0].tag)
        finally:
            sess.close()
